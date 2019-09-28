from django.shortcuts import render, HttpResponseRedirect
from .forms import ScriptsUserLoginForm, ScriptsUserRegisterForm, ScriptsUserEditForm
from django.contrib import auth
from django.urls import reverse

from authapp.models import UserRights

# Create your views here.

def login(request):
    title = 'вход'

    login_form = ScriptsUserLoginForm(data=request.POST or None)

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)

            return HttpResponseRedirect(reverse('admin:control_post'))

    content = {
        'title': title,
        'login_form': login_form
    }

    return render(request, 'authapp/login.html', content)

def register(request):
    title = 'регистрация'
    test_scripts_days = 30



    if request.method == 'POST':
        register_form = ScriptsUserRegisterForm(request.POST)

        if register_form.is_valid():
            # try:
            new_user = register_form.save()
            # except ValueError:
            #     content = {
            #         'title': title,
            #         'register_form': register_form
            #     }
            #
            #     return render(request, 'authapp/register.html', content)

            new_user.scripts_days += test_scripts_days
            new_user.save()
            user_rights = UserRights(user=new_user)
            user_rights.save()

            return HttpResponseRedirect(reverse('auth:login'))
        else:
            content = {
                'title': title,
                'register_form': register_form
            }

            return render(request, 'authapp/register.html', content)

    else:
        register_form = ScriptsUserRegisterForm()

    content = {
        'title': title,
        'register_form': register_form
    }

    return render(request, 'authapp/register.html', content)

def edit(request):
    title = 'редактировать'

    if request.method == 'POST':
        edit_form = ScriptsUserEditForm(request.POST, instance=request.user)

        if edit_form.is_valid:
            edit_form.save()

            return HttpResponseRedirect(reverse('auth:edit'))

    else:
        edit_form = ScriptsUserEditForm(instance=request.user)

    content = {
        'title': title,
        'edit_form': edit_form
    }

    return render(request, 'authapp/edit.html', content)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:main_page'))



