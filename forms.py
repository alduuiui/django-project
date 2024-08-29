from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError
from .models import Profile
from django.forms import ModelForm

class UserRegisterationForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):

        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)


        if user.exists():
           raise ValidationError("username already exists!....")
        return username
    

class UserLoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)


class FormUpdateProfile(forms.Form, ModelForm):
    email = forms.EmailField(widget=forms.EmailInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    class Meta:
        model = Profile
        fields = ('age', 'bio')