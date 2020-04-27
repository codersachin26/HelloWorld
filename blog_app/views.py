from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse
from .forms import MyUserForm,LoginForm,ArticleForm,MyAuthorForm
from .models import *
from django.contrib.auth import authenticate,login,logout
import json
from django.core import serializers






# Create your views here.

def index(request):
    new_blog = Article.objects.last()
    author = MyUser.objects.get(id=new_blog.author_id,is_author=True)
    related_articles = Article.objects.filter(category=new_blog.category,accessible=True)
    user = request.user
    cmts = UserComments.objects.filter(article_id=new_blog.id).order_by('-id')[:4]
    replys = ReplyComments.objects.filter(article_id=new_blog.id)
    likes = ArticleLikes.objects.filter(article_id=new_blog.id).count()
    userlike = ArticleLikes.objects.filter(article_id=new_blog.id,user_id=request.user.id).exists()
    if userlike:
        active='blue'
    else:
        active ='black'
    context = {'related_articles':related_articles,'active':active,'user':user,'new_blog':new_blog,'cmts':cmts,'replys':replys,'author':author,'likes':likes,'total_cmt':cmts.count()}
    return render(request,'index.html',context)

def all_blog(request):
    all_blog = Article.objects.all()
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
            newdata["cmt"] = UserComments.objects.filter(article_id=art.id).count()
            newdata["title"] = art.title
            newdata["id"] = art.id
            newdata["thumbnail"] = art.thumbnail
            newdata["like"] = ArticleLikes.objects.filter(article_id=art.id).count() + ReplyComments.objects.filter(article_id=art.id).count()
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
    if request.user.is_authenticated:
        u_cmt = UserComments()
        u_cmt.user_id = request.user.id
        u_cmt.article_id = article_id
        u_cmt.u_msg = request.POST['cmt-msg']
        u_cmt.u_name = request.user.username
        u_cmt.save()
        usercmt = UserComments.objects.last()
        serialized_obj = serializers.serialize('json', [usercmt])
        print(serialized_obj)
        data=serialized_obj.strip("[]")
        print(data)
   
        return JsonResponse(data,safe=False)

    else:
        return  JsonResponse({'ok':1,'url':'http://127.0.0.1:8000/user_register'})


def cmt_reply(request,article_id):
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
    if request.user.is_authenticated:
        if not ArticleLikes.objects.filter(article_id=article_id,user_id=request.user.id).exists():
            like = ArticleLikes()
            like.article_id = article_id
            like.user_id = request.user.id
            like.save()
            dict = {'ok':1}
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
    if userlike:
        active='blue'
    else:
        active ='black'
    context = {'related_articles':related_articles,'active':active,'user':user,'new_blog':view_blog,'cmts':cmts,'replys':replys,'author':author,'likes':likes,'total_cmt':cmts.count()}
    return render(request,'index.html',context)


def about(request):
    return render(request,'about.html')








        



    



    
