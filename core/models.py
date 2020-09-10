from django.db import models
import datetime


class Perfil(models.Model):

    nome = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)


class Empresa(models.Model):

    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    senha = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

class Funcionario(models.Model):

    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=20)
    empresas = models.ManyToManyField(Empresa)
    senha = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)


class Entrega(models.Model):

    descricao = models.CharField(max_length=100)
    anexo = models.CharField(max_length=250000)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='entregas')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='entregas')
    ativo = models.BooleanField(default=True)

class Localizacao(models.Model):

    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    data = models.DateTimeField(default=datetime.datetime.now())
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='localizacoes', null=True)
    entrega = models.OneToOneField(Entrega, on_delete=models.CASCADE, related_name='localizacao', null=True)

