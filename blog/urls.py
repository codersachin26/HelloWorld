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
    path('login',views.user_login,name='login'),
    path('more/<int:blog_id>',views.more,name="more"),
    path('about',views.about,name="about"),
    path('logout',views.user_logout),
    path('author_dashboard',views.author_dashboard,name="author_dashboard"),
    path('add_cmt1/<int:article_id>',views.add_cmt,name="addcmt1"),
    path('new_article',views.new_article),
    path('author_register',views.author_register),
    path('reply/<int:article_id>',views.cmt_reply,name='reply'),
    path('all_blog',views.all_blog,name="all_blogs"),
    path('like_article/<int:article_id>',views.like_article,name="like"),
    path('view_article/<int:article_id>',views.view_article,name="view_article"),
    path('notification',views.notifications,name='notification'),
    path('reset_password_form',views.reset_user_password,name='reset-password-form'),
    path('validated_token',views.validated_token,name='validated-token'),
    path('create_new_pass',views.create_new_password,name='create-new-password'),
    path('is_username_taken',views.is_username_valid,name='is-username-taken'),
    path('is_email_taken',views.is_email_valid,name='is-email-taken'),
    path('author_all_blog',views.author_all_blog,name='author-all-blog'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
