from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .forms import RegisterForm, AuthForm
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .models import Users
from django.contrib.auth import get_user_model, logout
from django.contrib.auth import login as login_auth
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse
from .decorators import not_authenticated


def register(request):
    if request.method == 'GET':
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})
    
    elif request.method == "POST":
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            form_new = register_form.save(commit=False)
            form_new.is_active = False
            form_new.save()
            # TODO: REDIRECIONAR PARA LOGIN
            return redirect(reverse('login'))
        else:
            return render(request, 'register.html', {'register_form': register_form})


def active_account(request, uidb4, token):
    User = get_user_model()
    uid = force_str(urlsafe_base64_decode(uidb4))
    user = User.objects.filter(pk=uid)

    if (user := user.first()) and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login_auth(request, user)
        messages.add_message(request, constants.SUCCESS, "Seu usuário foi ativo com sucesso.")
        return redirect(reverse('login'))
    else:
        messages.add_message(request, constants.ERROR, "A url acessada não é válida.")
        return redirect(reverse('login'))


@not_authenticated
def login(request):
    if request.method == 'GET':
        auth_form = AuthForm()
        return render(request, 'login.html', {'auth_form': auth_form})
    elif request.method == 'POST':
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            # Tem um usuário com esse email e senha
            if auth_form.is_valid():
                return redirect('/')
            
        messages.add_message(request, constants.ERROR, "Email ou senha incorretos.")
        return redirect(reverse('login'))
        # # auth.login(request, services)
        # return redirect(reverse('servicos'))
        # return render(request, 'login.html', {'auth_form': auth_form})

       
           

def logout_user(request):
    logout(request)
    messages.add_message(request, constants.SUCCESS, "Você foi deslogado")
    return redirect(reverse('login'))