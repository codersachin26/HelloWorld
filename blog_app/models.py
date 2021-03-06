from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import CustomUserManager




    


class MyUser(AbstractBaseUser,PermissionsMixin):
    f_name = models.CharField(max_length=20,null=True)
    s_name = models.CharField(max_length=20,null=True)
    email = models.EmailField(max_length=30, unique=True)
    username = models.CharField(max_length=25,unique=True)
    profile_pic = models.ImageField(upload_to='user_pic')
    date_joined = models.DateField(default=timezone.now)
    occupation = models.CharField(max_length=50,null=True)
    country = models.CharField(max_length=15,null=True)
    github_address = models.CharField(blank=True,max_length=50,null=True)
    linkedin_address = models.CharField(blank=True,max_length=50,null=True)
    instagram_address = models.CharField(blank=True,max_length=50,null=True)
    is_active = models.BooleanField(default=True)   
    is_author = models.BooleanField(default=False) 
    is_user = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=45)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.is_author:
            return 'Author '+self.username
        elif self.is_user:
            return 'User '+self.username
        else:
            self.is_author = True
            return 'admin '+self.email








class Blog(models.Model):
    type =(
        ("Programming","Programming"),
        ("Framework","Framework"),
        ("Hacking","Hacking"),
        ("Language","Language"),
        ("Other","Other"),

    )
    author = models.ForeignKey('MyUser',blank=True,null=True,on_delete=models.CASCADE)
    author_name = models.CharField(blank=True,max_length=25)
    title = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to='thumbnail_img/')
    upload_date = models.DateTimeField(blank=True,default=timezone.now)
    category = models.CharField(max_length=30,default="Other",choices=type)
    content = models.TextField(max_length=5000)
    accessible = models.BooleanField(blank=True,default=False)

    def __str__(self):
        return self.author_name+' '+self.title +' '+str(self.accessible)



class Comments(models.Model):
    user = models.ForeignKey('MyUser',blank=True,null=True,on_delete=models.CASCADE)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    cmt_msg = models.CharField(max_length=200)
    u_name = models.CharField(max_length=25)
    cmt_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.u_name


class CommentsReply(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    main_cmt = models.ForeignKey('Comments',on_delete=models.CASCADE)
    r_msg = models.CharField(max_length=200)
    u_name = models.CharField(max_length=25)
    cmt_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'subcmt '+ self.u_name

class Likes(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    user = models.ForeignKey('MyUser',on_delete=models.CASCADE)

    def __str__(self):
        return self.blog.title + ' ' + self.user.username



class Notification(models.Model):
    receiverID =   models.IntegerField()
    sender   =   models.ForeignKey('MyUser',on_delete=models.CASCADE)
    msg      =   models.CharField(max_length=200)
    is_read  =   models.BooleanField(default=False)
    is_del   =   models.BooleanField(default=False)

    def __str__(self):
        return self.receiverID


class Token(models.Model):
    token = models.IntegerField()
    userId = models.IntegerField()
    tokenID = models.IntegerField()
    is_valid = models.BooleanField(default=False)
