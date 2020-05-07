from django import forms
from .models import MyUser,Article

class MyAuthorForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['f_name','s_name','profile_pic','occupation','country','github_address','linkedin_address','username','email','password']


class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username','email','password','profile_pic']
class LoginForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email','password']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','thumbnail','category','content']

class Reset_PassWord_Form(forms.Form):
    email = forms.EmailField()

    def __str__(self):
        return self.email



