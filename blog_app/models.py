from django.db import models
from django.utils import timezone
from datetime import time

# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=25)
    email_id = models.EmailField()
    profile_pic = models.ImageField(upload_to='user_pic/')
    password = models.CharField(max_length=30)

    def __str__(self):
        return 'user '+self.username


class Author(models.Model):
    f_name = models.CharField(max_length=20)
    s_name = models.CharField(max_length=20)
    email_id = models.EmailField()
    occupation = models.CharField(max_length=50)
    country = models.CharField(max_length=15)
    gitgub_address = models.CharField(max_length=30)
    linkedin_address = models.CharField(max_length=30)
    password = models.CharField(max_length=25)
    profile_pic = models.ImageField(upload_to='author_pic/')
    authorise = models.BooleanField(default=False)

    def __str__(self):
        return 'Author '+self.f_name+' '+self.s_name+' '+self.authorise




class Article(models.Model):
    author = models.ForeignKey('Author',models.CASCADE,null=True)
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



