from django.contrib import admin
from .models import Article,Author,Users

# Register your models here.
admin.site.register(Author)
admin.site.register(Article)
admin.site.register(Users)