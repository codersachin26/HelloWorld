from django.contrib import admin
from .models import Article,MyUser,UserComments,Token

# Register your models here.
admin.site.register(Article)
admin.site.register(MyUser)
admin.site.register(UserComments)
admin.site.register(Token)