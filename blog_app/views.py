from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse
from .forms import *
from .models import *
from django.contrib.auth import authenticate,login,logout
import json
from django.core import serializers
from django.core.mail import send_mail
from blog.settings import EMAIL_HOST_USER
from datetime import datetime






# Create your views here.

def index(request):
    new_blog = Article.objects.last()
    author = MyUser.objects.get(id=new_blog.author_id)
    related_articles = Article.objects.filter(category=new_blog.category,accessible=True)
    user = request.user
    total_cmts = UserComments.objects.filter(article_id=new_blog.id).count()
    cmts = UserComments.objects.filter(article_id=new_blog.id).order_by('-id')[:4]
    morecount = UserComments.objects.all().count()
    if morecount > 4:
        more = True
        request.session['next'] = '2'
    else:
        more = False     
    replys = ReplyComments.objects.filter(article_id=new_blog.id)
    likes = ArticleLikes.objects.filter(article_id=new_blog.id).count()
    userlike = ArticleLikes.objects.filter(article_id=new_blog.id,user_id=request.user.id).exists()
    if userlike:
        active='blue'
    else:
        active ='black'

    if request.user.is_authenticated:
        unread = Notification.objects.filter(receiverID=request.user.id,is_read=False).count()
    else:
        unread =None

    context = {'unread':unread,'more':more,'related_articles':related_articles,'active':active,'user':user,'new_blog':new_blog,'cmts':cmts,'replys':replys,'author':author,'likes':likes,'total_cmt':total_cmts}
    return render(request,'index.html',context)

def all_blog(request):
    all_blog = Article.objects.filter(accessible=True)
    user = request.user
    return render(request,'all_blog.html',{'user':user,'all_blog':all_blog})




def author_dashboard(request):
    if request.user.is_author:
        articles = Article.objects.filter(author_id=request.user.id,accessible=True)
        panding_article = Article.objects.filter(author_id=request.user.id,accessible=False).count()
        accesible_article = articles.count()
        data = []
    
        for art in articles:
            newdata = {}
            newdata["cmt"] = UserComments.objects.filter(article_id=art.id).count() + ReplyComments.objects.filter(article_id=art.id).count()
            newdata["title"] = art.title
            newdata["id"] = art.id
            newdata["thumbnail"] = art.thumbnail
            newdata["like"] = ArticleLikes.objects.filter(article_id=art.id).count() 
            data.append(newdata)
        author = request.user

        context ={'data':data,'author':author,'articles':articles,'panding_article':panding_article,'accesible_article':accesible_article}
        return render(request,'Author_dashboard.html',context)
    else:
        raise Http404()


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            return HttpResponse('you are not log in')
    form = LoginForm
    return render(request,'login.html',{'form':form})

def user_logout(request):
    logout(request)
    return redirect('/')


def user_register(request):
    if request.method == 'POST':
        form = MyUserForm(request.POST,request.FILES)
        password = request.POST['password']
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(password)
            user.is_user = True
            user.save()
            login(request,user)
            return redirect('/')
        else:
            return HttpResponse('not done')
        
    else:
        form = MyUserForm()
        return render(request,'user_register.html',{'form':form})


def author_register(request):
    if request.method == 'POST':
        new_user = MyAuthorForm(request.POST,request.FILES)
        if new_user.is_valid():
            user=new_user.save(commit=False)
            password = request.POST['password']
            user.set_password(password)
            user.is_author = True
            user.save()
            login(request,user)
            return redirect('/')
        else:
            raise Http404()
        
    else:
        form = MyAuthorForm()
        return render(request,'author_register.html',{'form':form})

        

def add_cmt(request,article_id):
    if request.is_ajax():
        if request.user.is_authenticated:
            u_cmt = UserComments()
            u_cmt.user_id = request.user.id
            u_cmt.article_id = article_id
            u_cmt.u_msg = request.POST['cmt-msg']
            u_cmt.u_name = request.user.username
            u_cmt.save()
            usercmt = UserComments.objects.last()
            serialized_obj = serializers.serialize('json',[usercmt])
            data=serialized_obj.strip("[]")

            mk_notification = Notification()
            article = Article.objects.get(id=article_id)
            receiverID =article.author.id
            senderID = request.user
            mk_notification.receiverID = receiverID
            mk_notification.sender  =  senderID
            mk_notification.msg = request.user.username.upper()+' comment on your '+ article.title+' blog '+'"'+request.POST['cmt-msg']+'"'
            mk_notification.save()
    
            return JsonResponse(data,safe=False)

        else:
            return  JsonResponse({'ok':1,'url':'http://127.0.0.1:8000/user_register'})


def cmt_reply(request,article_id):
    if request.is_ajax():
        data = {}
        if request.user.is_authenticated:
            cmt_id = request.POST['cmt-id']
            print(cmt_id)
            r_cmt = ReplyComments()
            r_cmt.article_id = article_id
            r_cmt.main_cmt_id = cmt_id
            r_cmt.r_msg = request.POST['cmt-msg']
            r_cmt.u_name = request.user.username
            r_cmt.save()
            replytime = ReplyComments.objects.last().cmt_date
            data["cmt_date"] = replytime

            mk_notification = Notification()
            cmt = UserComments.objects.get(id=cmt_id)
            article = Article.objects.get(id=article_id)
            receiverID = cmt.user.id
            senderID = request.user
            mk_notification.receiverID = receiverID
            mk_notification.sender  =  senderID
            mk_notification.msg = request.user.username.upper()+' reply on your comment "'+cmt.u_msg+'" on blog '+article.title+'"'+request.POST['cmt-msg']+'"'
            mk_notification.save()
    
            return JsonResponse(data,safe=False)

        else:
            return JsonResponse({'ok':1,'url':'http://127.0.0.1:8000/user_register'})



def new_article(request):
    if request.user.is_author:
        if request.method == 'POST':
            articleform  = ArticleForm(request.POST,request.FILES)
            if articleform.is_valid():
                article = articleform.save(commit=False)
                article.author_id = request.user.id
                article.author_name = request.user.username
                article.save()
                return redirect('/author_dashboard')
            else:
                raise Http404()
        else:
            form = ArticleForm()
            return render(request,'New_article.html',{'form':form})
    else:
        raise Http404()



def like_article(request,article_id):
    if request.is_ajax():
        if request.user.is_authenticated:
            if not ArticleLikes.objects.filter(article_id=article_id,user_id=request.user.id).exists():
                like = ArticleLikes()
                like.article_id = article_id
                like.user_id = request.user.id
                like.save()
                dict = {'ok':1}

                mk_notification = Notification()
                # cmt = UserComments.objects.get(id=cmt_id)
                article = Article.objects.get(id=article_id)
                receiverID = article.author.id
                senderID = request.user
                mk_notification.receiverID = receiverID
                mk_notification.sender  =  senderID
                mk_notification.msg = request.user.username.upper()+' like your '+article.title+' blog '
                mk_notification.save()
            
                return HttpResponse(json.dumps(dict), content_type='application/json')
            else:
                like = ArticleLikes.objects.get(article_id=article_id,user_id=request.user.id)
                like.delete()
                dict = {'ok':1}
                return HttpResponse(json.dumps(dict), content_type='application/json')
                
        else:
            return JsonResponse({'ok':0,'url':'http://127.0.0.1:8000/user_register'})

    


def view_article(request,article_id):
    view_blog = Article.objects.get(id=article_id)
    author = MyUser.objects.get(id=view_blog.author_id,is_author=True)
    related_articles = Article.objects.filter(category=view_blog.category,accessible=True)
    user = request.user
    cmts = UserComments.objects.filter(article_id=view_blog.id).order_by('-id')[:4]
    replys = ReplyComments.objects.filter(article_id=view_blog.id)
    likes = ArticleLikes.objects.filter(article_id=view_blog.id).count()
    userlike = ArticleLikes.objects.filter(article_id=view_blog.id,user_id=request.user.id).exists()
    morecount = UserComments.objects.filter(article_id=view_blog.id).count()
    print(morecount)

    if morecount > 4:
        more = True
        request.session['next'] = '2'
    else:
        more = False 

    if userlike:
        active='blue'
    else:
        active ='black'
    context = {'more':more,'related_articles':related_articles,'active':active,'user':user,'new_blog':view_blog,'cmts':cmts,'replys':replys,'author':author,'likes':likes,'total_cmt':morecount}
    return render(request,'index.html',context)


def about(request):
    return render(request,'about.html')



def more(request,blog_id):
    if request.is_ajax():
        user_cmts ={}
        no = int(request.session['next']) 
        more = False
        c = UserComments.objects.filter(article_id=blog_id).order_by('-id').count()
        cmts = UserComments.objects.filter(article_id=blog_id).order_by('-id')[(no-1)*4:no*4]
        next = UserComments.objects.filter(article_id=blog_id).order_by('-id')[((no)*4):(no+1)*4].exists()
        all_cmts = []
        for cmt in cmts:
            user_cmts ={}
            usercmt = {
                'profile_pic':str(cmt.user.profile_pic),
                'username': cmt.u_name,
                'cmtmsg': cmt.u_msg,
                'article_id': cmt.article.id,
                'cmt_date' :  str(cmt.cmt_date),
                'id' : cmt.id
            }
            user_cmts['cmt'] = usercmt
            replylist = []
            replys = ReplyComments.objects.filter(article_id=blog_id,main_cmt=cmt.id)
            for rply in replys:
                reply = {
                'profile_pic': str(rply.main_cmt.user.profile_pic),
                'username': rply.u_name,
                'r_msg': rply.r_msg,
                'cmt_id': cmt.id,
                'article_id': rply.article.id,
                'cmt_date' :  str(rply.cmt_date)
                }
                replylist.append(reply)
            user_cmts['reply'] = replylist
            all_cmts.append(user_cmts)

        nextpage = no+1 
        if not next:
            more = True
        else:
            request.session['next'] = str(no+1)

        data = {
        'usercmts':all_cmts,
        'more':more
        }
        
        return HttpResponse(json.dumps(data),content_type='application/json')




def notifications(request):
    notification = Notification.objects.filter(receiverID=request.user.id,is_del=False).order_by('-id')[:10]
    un_read = Notification.objects.filter(receiverID=request.user.id,is_del=False,is_read=False)
    for r in un_read:
        r.is_read = True
        r.save()

    return render(request,'notification.html',{'notification':notification})



def reset_user_password(request):
    if request.method == 'POST':
        user =  Reset_PassWord_Form(request.POST)
        if MyUser.objects.filter(email=user['email'].value()).exists():
            subject = 'Reset Password'
            message = "Don't share this code to anyone!  \n CODE = 8888 "
            recepient = str(user['email'].value())
            new_token = Token()
            tokenID = int(datetime.utcnow().timestamp())
            userID = MyUser.objects.get(email=user['email'].value()).id
            new_token.tokenID =  tokenID
            new_token.token = 8888
            new_token.userId = userID
            new_token.save()
            # token_id = Token.objects.get(userId=userID,id=tokenID)
            request.session['token_id'] = str(tokenID)
            send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)
            return render(request, 'valid_token.html')
        else:
            return HttpResponse('wrong email id')
    else:
        form =  Reset_PassWord_Form()
        return render(request, 'pass_reset_form.html', {'form':form})


def validated_token(request):
    if request.method == 'POST':
        token = int(request.POST.get('token'))
        print(token)
        print(type(token))
        token_id = int(request.session['token_id'])
        valid_token = Token.objects.get(tokenID=token_id)
        print(valid_token.token)
        print(valid_token.tokenID)
        print(type(valid_token.token))
        if token == valid_token.token:
            valid_token.is_valid = True
            return render(request, 'create_new_pass.html')
        else:
            return HttpResponse('not valid token') 



def create_new_password(request): 
    token_id = int(request.session['token_id'])
    is_valid = Token.objects.get(tokenID=token_id)
    if is_valid:
        new_pass = request.POST.get('pass1')
        user = MyUser.objects.get(id=is_valid.userId)
        user.set_password(new_pass)
        user.save()
        return HttpResponse('done')
    else:
        return HttpResponse('not valid user')
   


        



    



    
