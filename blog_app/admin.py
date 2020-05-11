from django.contrib import admin
from .models import Blog,MyUser,Comments,Token

# Register your models here.
admin.site.register(Blog)
admin.site.register(MyUser)
admin.site.register(Comments)
admin.site.register(Token)