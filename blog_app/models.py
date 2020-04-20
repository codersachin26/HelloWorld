from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import CustomUserManager




    


class MyUser(AbstractBaseUser,PermissionsMixin):
    f_name = models.CharField(blank=True,max_length=20,null=True)
    s_name = models.CharField(blank=True,max_length=20,null=True)
    email = models.CharField(max_length=40, unique=True)
    username = models.CharField(max_length=25,unique=True)
    profile_pic = models.ImageField(upload_to='user_pic')
    date_joined = models.DateField(default=timezone.now)
    occupation = models.CharField(blank=True,max_length=50,null=True)
    country = models.CharField(blank=True,max_length=15,null=True)
    authorise = models.BooleanField(default=False)
    github_address = models.CharField(blank=True,max_length=50,null=True)
    linkedin_address = models.CharField(blank=True,max_length=30,null=True)
    is_active = models.BooleanField(default=True)   
    is_author = models.BooleanField(default=False) 
    is_user = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=25)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.is_author:
            return 'Author '+self.username
        elif self.is_user:
            return 'User '+self.username
        else:
            return self.username








class Article(models.Model):
    author = models.ForeignKey('MyUser',blank=True,null=True,on_delete=models.CASCADE)
    author_name = models.CharField(blank=True,max_length=25)
    title = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to='thumbnail_img/')
    upload_date = models.DateTimeField(blank=True,default=timezone.now)
    category = models.CharField(max_length=30)
    content = models.CharField(max_length=5000)
    accessible = models.BooleanField(blank=True,default=False)

    def __str__(self):
        return self.author_name+' '+self.title +' '+str(self.accessible)



class UserComments(models.Model):
    user = models.ForeignKey('MyUser',blank=True,null=True,on_delete=models.CASCADE)
    article = models.ForeignKey('Article',on_delete=models.CASCADE)
    u_msg = models.CharField(max_length=200)
    u_name = models.CharField(max_length=25)
    cmt_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.u_name


class ReplyComments(models.Model):
    article = models.ForeignKey('Article',on_delete=models.CASCADE)
    main_cmt = models.ForeignKey('UserComments',on_delete=models.CASCADE)
    r_msg = models.CharField(max_length=200)
    u_name = models.CharField(max_length=25)
    cmt_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'subcmt '+ self.u_name

