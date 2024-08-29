from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterationForm, UserLoginForm
from django.contrib.auth.models import User
from typing import Any
from django.http import HttpRequest
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FormUpdateProfile




class RegisterView(View):   
    form_register = UserRegisterationForm
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):

        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
         

    def get(self, request):

        return render(request, 'account/register.html', context={'form': self.form_register}) 


    def post(self, request):

        form_register = UserRegisterationForm(request.POST)

        if form_register.is_valid():
            
            data_register = form_register.cleaned_data
            user = User.objects.create_user(
                username=data_register['username'],
                email=data_register['email'],
                password=data_register['password'],

            )
            if user:

                return redirect('home')
            

class LoginView(View):


    template_name = 'account/login.html'
    form_Login = UserLoginForm

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):

        return render(request, self.template_name, context={'form': self.form_Login})

    def post(self, request):

        form_Login = self.form_Login(request.POST)

        if form_Login.is_valid():
            data_login = form_Login.cleaned_data
            
            user = authenticate(
                username=data_login['username'],
                password=data_login['password']
            )

            if user:
                login(request, user)
                return redirect('home')
                
            else:
                return redirect('login')
            
        else:
            return render(request, template_name='account/login.html')
        



class LogoutView(LoginRequiredMixin ,View):

    def get(self, request):

        logout(request)
        return redirect('home')
    

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, id):
        user = User.objects.get(id=id)
        return render(request, 'account/profile.html', context={'user': user})
    

class UpdateProfileView(LoginRequiredMixin, View):
    form = FormUpdateProfile
    def get(self, request):
        form = self.form(instance=request.user)

        return render(request, 'account/update_profile.html', context={'form': form})

    def post(self, request):
        profile = request.user.profile
        form = self.form(request.POST, instance=profile)
        if form.is_valid():
            email = form.cleaned_data['email']
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']


            request.user.email = email
            request.user.last_name = last_name
            request.user.first_name = first_name
            request.user.save()

            form.save()
            return redirect('home')
        return redirect('home')



