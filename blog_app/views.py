from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from .forms import MyUserForm,LoginForm,ArticleForm,MyAuthorForm
from .models import *
from django.contrib.auth import authenticate,login,logout







# Create your views here.

def index(request):
    new_blog = Article.objects.first()
    user = request.user
    cmts = UserComments.objects.filter(article_id=new_blog.id)
    replys = ReplyComments.objects.filter(article_id=new_blog.id)
    return render(request,'index.html',{'user':user,'new_blog':new_blog,'cmts':cmts,'replys':replys})

def all_blog(request):
    all_blog = Article.objects.all()
    user = request.user
    return render(request,'all_blog.html',{'user':user,'all_blog':all_blog})




def author_dashboard(request):
    if request.user.is_author:
        return render(request,'Author_dashboard.html')
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
        form = MyUserForm(request.POST)
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
        new_user = MyUser()
        password = request.POST['password']
        new_user.set_password(password)
        new_user.username = request.POST['username']
        new_user.email = request.POST['email']
        new_user.profile_pic = request.POST['profile_pic']
        new_user.f_name = request.POST['f_name']
        new_user.s_name = request.POST['s_name']
        new_user.occupation = request.POST['occupation']
        new_user.country = request.POST['country']
        new_user.github_address = request.POST['github_address']
        new_user.linkedin_address = request.POST['linkedin_address'] 
        new_user.is_author = True
        new_user.save()
        login(request,new_user)
        return redirect('/')
        
    else:
        form = MyAuthorForm()
        return render(request,'author_register.html',{'form':form})

        

def add_cmt(request,article_id):
    if request.user.is_authenticated:
        u_cmt = UserComments()
        u_cmt.article_id = article_id
        u_cmt.u_msg = request.POST['cmt-msg']
        u_cmt.u_name = request.user.username
        u_cmt.save()
        return redirect('/')

    else:
        raise Http404()

def cmt_reply(request,cmt_id,article_id):
    if request.user.is_authenticated:
        r_cmt = ReplyComments()
        r_cmt.article_id = article_id
        r_cmt.main_cmt_id = cmt_id
        r_cmt.r_msg = request.POST['r-msg']
        r_cmt.u_name = request.user.username
        r_cmt.save()
        return redirect('/')

    else:
        raise Http404()



def new_article(request):
    if request.user.is_author:
        if request.method == 'POST':
            article = Article()
            article.authorID = request.user.id
            article.author_name = request.user.username
            article.title  =  request.POST['title']
            article.category  =   request.POST['category']
            article.thumbnail  =  request.POST['thumbnail']
            article.content =  request.POST['content']
            article.save()
            return HttpResponse('done')
        else:
            form = ArticleForm()
            return render(request,'New_article.html',{'form':form})
    else:
        raise Http404()





    
