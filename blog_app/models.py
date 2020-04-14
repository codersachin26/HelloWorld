from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import CustomUserManager





class MyUser(AbstractBaseUser,PermissionsMixin):
    f_name = models.CharField(max_length=20,null=True)
    s_name = models.CharField(max_length=20,null=True)
    email = models.CharField(max_length=40, unique=True)
    username = models.CharField(max_length=25,unique=True)
    profile_pic = models.ImageField(upload_to='user_pic')
    date_joined = models.DateField(default=timezone.now)
    occupation = models.CharField(max_length=50,null=True)
    country = models.CharField(max_length=15,null=True)
    authorise = models.BooleanField(default=False)
    github_address = models.CharField(max_length=30,null=True)
    linkedin_address = models.CharField(max_length=30,null=True)
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
            return 'Author '+self.f_name+' '+self.s_name+str(self.authorise)
        elif self.is_user:
            return 'User '+self.username
        else:
            return self.email








class Article(models.Model):
    authorID = models.IntegerField()
    author_name = models.CharField(max_length=25)
    title = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to='thumbnail_img/')
    upload_date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=30)
    content = models.CharField(max_length=5000)
    accessible = models.BooleanField(default=False)

    def __str__(self):
        return 'ID '+self.author_id+' '+self.title



