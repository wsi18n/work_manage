from django.shortcuts import render, redirect, reverse
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse
from .models import *
from rbac import models as rbac_model
from django.contrib.auth import authenticate, login, logout

class Login(View):

    def get(self, request):
        if not request.session.get('username'):
            response =  render(request, 'users/login.html')
            response['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            return redirect('workbench:index')


    def post(self, request):
        temp_name = request.POST['username']
        temp_password = request.POST['password']
        # redirect_to = request.GET.get('next', '/')
        if temp_name and temp_password:
            try:
                user = UserProfile.objects.get(username=temp_name)
                if user.password == temp_password:
                    login(request,user)

                    return redirect(reverse('workbench:index'))
                else:
                    message = '密码不正确'
            except Exception as e :
                print(e)
                message = "用户不存在"
        response =  render(request, 'users/login.html', {'message': message})
        response['Access-Control-Allow-Origin'] = '*'
        return response

class Logout(View):

    def get(self, request):
        request.session.clear()
        # logout(request)
        return redirect('login')


class Index(View):
    def get(self, request):
        return redirect('workbench:index')


