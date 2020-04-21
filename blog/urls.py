"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog_app import views
from . import  settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('user_register',views.user_register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('author_dashboard',views.author_dashboard),
    path('add_cmt/<int:article_id>',views.add_cmt),
    path('new_article',views.new_article),
    path('author_register',views.author_register),
    path('reply/<int:cmt_id>/<int:article_id>',views.cmt_reply),
    path('all_blog',views.all_blog),
    path('like_article/<int:article_id>',views.like_article,name="like"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
