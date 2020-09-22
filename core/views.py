from django.shortcuts import render, redirect, Http404
from django.contrib.auth import authenticate, login as logar, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from . import models
from django.db import connection

@login_required(login_url='/login')

def inicio(request):
    if request.GET.get('busca'):        
        with connection.cursor() as cursor:
            cursor.executescript("SELECT * FROM core_comentario WHERE titulo LIKE '%%{}%%';".format(request.GET.get('busca')))
            comentarios = cursor.fetchall()
        contexto = {'comentarios': comentarios, 'busca': request.GET.get('busca')}
    else:
        contexto = {'comentarios': models.Comentario.objects.all().order_by('-data')}
    return render(request, 'index.html', contexto)

def login(request):
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

def cadastrar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'cadastrar.html', {})

    if request.method == 'POST':
        try:
            if(User.objects.filter(username=request.POST.get('email', '')).exists()):
                messages.success(request, 'Email já cadastrado. Utilize outro email.')
                return render(request, 'cadastrar.html', {'email': request.POST.get('email'), 'nome': request.POST.get('nome'), 'sobrenome': request.POST.get('sobrenome')})
            else:
                usuario = User.objects.create_user(request.POST.get('email', ''), request.POST.get('email', ''), request.POST.get('senha', ''))
                usuario.first_name = request.POST.get('nome', '')
                usuario.last_name = request.POST.get('sobrenome', '')
                usuario.save()  
                messages.success(request, 'Conta criada com sucesso. Faça Login')
                return redirect('/login')
        except:
            messages.success(request, 'Não foi possível criar o cadastro. Tente novamente.')
            return render(request, 'cadastrar.html', {'email': request.POST.get('email'), 'nome': request.POST.get('nome'), 'sobrenome': request.POST.get('sobrenome')})

@login_required(login_url='/login')
def deslogar(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def cadastrar_comentario(request):
    try:
        models.Comentario.objects.create(autor=request.user, titulo=request.POST.get('titulo',''), texto=request.POST.get('texto',''))
        messages.success(request, 'Comentário criado com sucesso.')
    except:
        messages.success(request, 'Não foi possível criar o comentário. Tente novamente.')
    return redirect('/')