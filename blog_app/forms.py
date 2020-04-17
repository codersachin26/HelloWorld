from django import forms
from .models import MyUser

class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username','email','password','is_author']

class LoginForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email','password']



