from django import forms
from .models import MyUser,Test1

class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['f_name','s_name','username','occupation','country','is_author','email','password']

class LoginForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email','password']



