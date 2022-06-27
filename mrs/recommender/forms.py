from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.models import User

#login form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus' : True, 'class' : 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'class' : 'form-control'}))


#signup form
class UserSignUpForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password', widget = forms.PasswordInput(attrs={'class' : 'form-control'}))
    class meta :
        model = User
        fields = ['username', 'email']
        labels = {'email' : 'Email'}
        widgets = {'username' : forms.TextInput(attrs={'class' : 'form-control'})}