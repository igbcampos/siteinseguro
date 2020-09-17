from django.shortcuts import render

def inicio(request):
    contexto = {}
    return render(request, 'index.html', contexto)