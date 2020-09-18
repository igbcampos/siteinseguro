from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name= 'inicio'), 
    path('login', views.login, name= 'login'), 
    path('cadastrar', views.cadastrar, name= 'cadastrar'),
    path('deslogar', views.deslogar, name= 'deslogar'),
    path('cadastrar-comentario', views.cadastrar_comentario, name= 'cadastrar_comentario'),
]
