from django.contrib import admin
from core import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='inicio'),
    path('entrar/', views.entrar, name='entrar'),
    path('sair/', views.sair, name='sair'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('empresas', views.listar_empresas, name='listar_empresas'),
    path('funcionarios', views.listar_funcionarios, name='listar_funcionarios'),
    path('entregas', views.listar_entregas, name='listar_entregas'),
    path('entrega/<int:id_entrega>/excluir', views.excluir_entrega, name='excluir_entrega'),
    path('empresa/<int:id_empresa>/excluir', views.excluir_empresa, name='excluir_empresa'),
    path('funcionario/<int:id_funcionario>/excluir', views.excluir_funcionario, name='excluir_funcionario'),
    path('editar/entregas', views.editar_entregas, name='editar_entregas'),
    path('editar/empresas', views.editar_empresas, name='editar_empresas'),
    path('editar/funcionarios', views.editar_funcionarios, name='editar_funcionarios'),
]