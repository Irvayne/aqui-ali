from django.contrib import admin
from core import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='inicio'),
    path('entrar/', views.entrar, name='entrar'),
    path('sair/', views.sair, name='sair'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('carga/', views.carga, name='carga'),
    path('empresas', views.listar_empresas, name='listar_empresas'),
    path('funcionarios', views.listar_funcionarios, name='listar_funcionarios'),
    path('entregas', views.listar_entregas, name='listar_entregas'),
]