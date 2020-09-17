from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as logar, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

@login_required(login_url='/login')

def inicio(request):
    contexto = {}
    return render(request, 'index.html', contexto)

def login(request):
    contexto = {}
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'login.html', {})

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        usuario = authenticate(request, username=email, password=senha)
    
        if usuario is not None:
            logar(request, usuario)
            return redirect('/')
        else:
            contexto = {'email': email, 'mensagem': 'Usuário ou senha inválidos. Por favor, tente novamente.'}
            
            return render(request, 'login.html', contexto)
    else:
        raise Http404('Método de requisição não aceito')    