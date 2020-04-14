from django.contrib import admin
from .models import Article,MyUser

# Register your models here.
admin.site.register(Article)
admin.site.register(MyUser)