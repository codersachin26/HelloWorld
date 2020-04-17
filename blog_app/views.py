from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from .forms import MyUserForm,LoginForm
from .models import *
from django.contrib.auth import authenticate,login,logout







# Create your views here.

def index(request):
    user = request.user
    return render(request,'index.html',{'user':user})

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
            user.save()
            login(request,user)
            return redirect('/')
        else:
            return HttpResponse('not done')
        
    else:
        form = MyUserForm()
        return render(request,'user_register.html',{'form':form})

        

def add_cmt(request,id):
    if request.user.is_authenticated:
        u_cmt = UserComments()
        u_cmt.article = id
        u_cmt.u_msg = request.POST['cmt-msg']
        u_cmt.u_Email = request.user.email
        u_cmt.u_name = request.uset.username
        u_cmt.save()

    else:
        raise Http404()




    
