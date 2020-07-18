from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt

from core.models import Funcionario, Entrega, Perfil, Localizacao, Empresa
import datetime
import base64

@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            string = request.data
            cpf = string['cpf']
            senha = string['senha']

            try:
                func = Funcionario.objects.get(cpf = cpf, senha=senha)
                funcionario = populaObjetoFuncionario(func)

                map = {}
                map["sucesso"] = True
                map["mensagem"] = "Funcionario encontrado!"
                map["funcionario"] = funcionario
                return Response(map)
            except:
                map = {}
                map["sucesso"] = False
                map["mensagem"] = "Funcionario não encontrado!"
                map["funcionario"] = None
                return Response(map)
        except:
            return Response({'result': 'Requisicoes devem ser POST com o cpf e senha enviado no body'})
    return Response({'result': 'Requisicoes devem ser POST com o cpf e senha enviado no body'})



@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
@csrf_exempt
def buscarFuncionarios(request):
    string = request.data
    listaFuncionarios = []
    funcionario = {}
    funcionario["id"] = 0
    funcionario["nome"] = 'Todos'
    listaFuncionarios.append(funcionario)
    if string == 0:
        funcionarios = Funcionario.objects.all()
        for f in funcionarios:
            funcionario = {}
            funcionario["id"] = f.id
            funcionario["nome"] = f.nome
            for loc in f.localizacoes.all():
                funcionario["latitude"] = loc.latitude
                funcionario["longitude"] = loc.longitude
            listaFuncionarios.append(funcionario)
        return Response(listaFuncionarios)
    else:

        funcionarios = Funcionario.objects.all()
        for f in funcionarios:
            valido = False
            for emp in f.empresas.all():
                if emp.id == int(string):
                    valido = True

            funcionario = {}
            funcionario["id"] = f.id
            funcionario["nome"] = f.nome
            for loc in f.localizacoes.all():
                funcionario["latitude"] = loc.latitude
                funcionario["longitude"] = loc.longitude
            if valido:
                listaFuncionarios.append(funcionario)
        return Response(listaFuncionarios)






@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
@csrf_exempt
def todasEmpresas(request):
    listaEmpresas = []
    empresas = []
    if request.session['empresa'] == False:
        empresas = Empresa.objects.all()
        empresa = {}
        empresa["id"] = 0
        empresa["nome"] = "Todas"
        listaEmpresas.append(empresa)
    else:
        empresas.append(Empresa.objects.get(id=request.session['id_empresa']))
    for emp in empresas:
        empresa = {}
        empresa["id"] = emp.id
        empresa["nome"] = emp.nome
        listaEmpresas.append(empresa)
    return Response(listaEmpresas)




@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
@csrf_exempt
def atualizaDados(request):
    if request.method == 'POST':
        try:
            string = request.data
            id = string['id']

            try:
                func = Funcionario.objects.get(id=id)
                funcionario = populaObjetoFuncionario(func)

                map = {}
                map["sucesso"] = True
                map["mensagem"] = "Funcionario encontrado!"
                map["funcionario"] = funcionario
                return Response(map)
            except:
                map = {}
                map["sucesso"] = False
                map["mensagem"] = "Funcionario não encontrado!"
                map["funcionario"] = None
                return Response(map)
        except:
            return Response({'result': 'Requisicoes devem ser POST com o id enviado no body'})
    return Response({'result': 'Requisicoes devem ser POST com o id enviado no body'})


@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
@csrf_exempt
def atualizaLocalizacao(request):
    if request.method == 'POST':
        try:
            string = request.data
            id = string['id']
            l = string['localizacao']

            funcionario = Funcionario.objects.get(id=id)
            loc = funcionario.localizacoes.all()[0]
            loc.latitude = l["latitude"]
            loc.longitude = l["longitude"]
            loc.data = l["data"]
            loc.save()

            map = {}
            map["sucesso"] = True
            map["mensagem"] = "Localizacao salva com sucesso!"
            return Response(map)
        except:
            return Response({'result': 'Requisicoes devem ser POST com o id, e o objeto localizacao enviado no body'})
        return Response({'result': 'Requisicoes devem ser POST com o id, e o objeto localizacao enviado no body'})


@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
@csrf_exempt
def recebeImagem(request):
    if request.method == 'POST':
        data = request.data
        imgdata = base64.b64decode(data['imagem'])
        filename = 'teste.png'  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)
        map = {}
        map["sucesso"] = True
        map["mensagem"] = "Localizacao salva com sucesso!"
        return Response(map)



@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
@csrf_exempt
def finalizaEntrega(request):
    if request.method == 'POST':
        try:
            string = request.data
            id_empresa = string['id_empresa']
            id_funcionario = string['id_funcionario']
            entrega = string['entrega']
            localizacao = entrega['localizacao']

            print(entrega['localizacao'])

            ent = Entrega()
            ent.descricao = entrega["descricao"]
            ent.anexo = entrega["anexo"]
            ent.funcionario = Funcionario.objects.get(id=id_funcionario)
            ent.empresa = Empresa.objects.get(id=id_empresa)
            ent.save()

            loc = Localizacao()
            loc.latitude = localizacao['latitude']
            loc.longitude = localizacao['longitude']
            loc.data = localizacao['data']
            loc.entrega = ent
            loc.save()

            map = {}
            map["sucesso"] = True
            map["mensagem"] = "Entrega salva com sucesso!"
            return Response(map)
        except:
            return Response({'result': 'Requisicoes devem ser POST com o id, e o objeto localizacao enviado no body'})
        return Response({'result': 'Requisicoes devem ser POST com o id, e o objeto localizacao enviado no body'})


def populaObjetoFuncionario(func):
    funcionario = {}
    funcionario["id"] = func.id
    funcionario["cpf"] = func.cpf
    funcionario["nome"] = func.nome
    funcionario["senha"] = func.senha
    listaEmpresas = []
    listaEntregas = []
    listaLocalizacoes = []

    for emp in func.empresas.all():
        empresa = {}
        empresa["id"] = emp.id
        empresa["nome"] = emp.nome
        empresa["descricao"] = emp.descricao
        empresa["cnpj"] = emp.cnpj
        empresa["telefone"] = emp.telefone
        listaEmpresas.append(empresa)

    funcionario["empresas"] = listaEmpresas

    for entr in func.entregas.all():
        ent = {}
        ent["descricao"] = entr.descricao
        ent["id_empresa"] = entr.empresa.id
        localizacao = entr.localizacao
        l = {}
        l["latitude"] = localizacao.latitude
        l["longitude"] = localizacao.longitude
        l["data"] = localizacao.data
        ent["localizacao"] = l

        listaEntregas.append(ent)

    funcionario["entregas"] = listaEntregas

    for loc in func.localizacoes.all():
        loca = {}
        loca["latitude"] = loc.latitude
        loca["longitude"] = loc.longitude
        loca["data"] = loc.data
        listaLocalizacoes.append(loca)

    funcionario["localizacoes"] = listaLocalizacoes
    return funcionario