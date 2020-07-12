
from webservice import views
from django.urls import path, include


urlpatterns = [
    path('api/login/', views.login),
    path('api/atualiza/funcionario', views.atualizaDados),
    path('api/atualiza/localizacao', views.atualizaLocalizacao),
    path('api/finaliza/entrega', views.finalizaEntrega),
    path('api/empresas', views.todasEmpresas),
    path('api/funcionarios', views.buscarFuncionarios),
    path('api/imagem', views.recebeImagem),
]