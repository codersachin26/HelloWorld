from django.shortcuts import render
from django.http import HttpResponse





# Create your views here.

def index(request):
    return render(request,'index.html')

def author_login(request):
    	pass


def user_register(request):
    pass
