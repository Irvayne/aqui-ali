
from django.shortcuts import render, redirect
from core.models import Perfil, Empresa, Funcionario, Entrega, Localizacao
from core.carga import realizarCarga
from datetime import datetime


def home(request):
	return render(request, 'index.html')

def excluir_entrega(request, id_entrega):
    if verificaLogin(request) == False:
        return render(request, 'entrar.html')
    entrega = Entrega.objects.get(id=id_entrega)
    entrega.ativo = False
    entrega.save()
    return redirect('listar_entregas')

def excluir_funcionario(request, id_funcionario):
    if verificaLogin(request) == False:
        return render(request, 'entrar.html')
    funcioario = Funcionario.objects.get(id=id_funcionario)
    funcioario.ativo = False
    funcioario.save()
    return redirect('listar_funcionarios')

def excluir_empresa(request, id_empresa):
    if verificaLogin(request) == False:
        return render(request, 'entrar.html')
    empresa = Empresa.objects.get(id=id_empresa)
    empresa.ativo = False
    empresa.save()
    return redirect('listar_empresas')

def entrar(request):
    if request.method == 'POST':
        login = request.POST['login']
        senha = request.POST['senha']
        if login == 'amlogistica.the@gmail.com' and senha == '@qui@li*2020':
            request.session['login'] = 'amlogistica.the@gmail.com'
            request.session['senha'] = '@qui@li*2020'
            request.session['nome'] = 'AM Logística'
            request.session['empresa'] = False
            return redirect('dashboard')
        try:
            perfil = Perfil.objects.get(login = login, senha=senha)
            request.session['login'] = login
            request.session['senha'] = senha
            request.session['nome'] = perfil.nome
            request.session['empresa'] = False
            return redirect('dashboard')
        except:
            try:
                empresa = Empresa.objects.get(cnpj=login, senha=senha)
                request.session['login'] = login
                request.session['senha'] = senha
                request.session['id_empresa'] = empresa.id
                request.session['nome'] = empresa.nome
                request.session['empresa'] = True
                return redirect('dashboard')
            except:
                return render(request, 'entrar.html', {'message': 'Usuário e/ou senha inválidos!'})
    return render(request, 'entrar.html')

def verificaLogin(request):
    try:
       login = request.session['login']
       senha = request.session['senha']
       print('>>> login:' +login+" >>>> senha: "+senha)
       return True
    except:
        print('>>> acesso negado')
        return False

def sair(request):
    request.session['login'] = None
    request.session['senha'] = None
    request.session['id_empresa'] = None
    request.session['empresa'] = None
    request.session['nome'] = None
    return render(request, 'entrar.html')

def editar_entregas(request):
    if verificaLogin(request) == False:
        return render(request, 'entrar.html')
    id_entrega = request.POST['id_entrega']
    entrega = Entrega.objects.get(id=int(id_entrega))
    entrega.descricao = request.POST['descricao']
    entrega.save()
    return redirect('listar_entregas')


def dashboard(request):
    if verificaLogin(request) == False:
        return render(request, 'entrar.html')
    return render(request, 'dashboard.html')

def listar_empresas(request):
    if verificaLogin(request) == False:
        return render(request, 'entrar.html')
    if request.session['empresa'] == True:
        return redirect('dashboard')
    if request.method == 'POST':

        empresa = Empresa()
        empresa.nome = request.POST['nome']
        empresa.descricao = request.POST['descricao']
        empresa.cnpj = request.POST['cnpj']
        empresa.senha = request.POST['senha']
        empresa.telefone = request.POST['telefone']
        empresa.save()

        return redirect('listar_empresas')
    else:
        empresas = Empresa.objects.filter(ativo=True).all()
    return render(request, 'empresas.html', {'empresas': empresas} )

def editar_empresas(request):
    if verificaLogin(request) == False:
        return render(request, 'entrar.html')
    id_empresa = request.POST['id_empresa']
    empresa = Empresa.objects.get(id=int(id_empresa))
    empresa.nome = request.POST['nome']
    empresa.descricao = request.POST['descricao']
    empresa.cnpj = request.POST['cnpj']
    empresa.senha = request.POST['senha']
    empresa.telefone = request.POST['telefone']
    empresa.save()

    return redirect('listar_empresas')

def editar_funcionarios(request):
    if verificaLogin(request) == False:
        return render(request, 'entrar.html')
    id_funcionario = request.POST['id_funcionario']
    funcionario = Funcionario.objects.get(id=int(id_funcionario))

    funcionario.nome = request.POST['nome']
    funcionario.cpf = request.POST['cpf']
    funcionario.senha = request.POST['senha']
    empresas = Empresa.objects.all()
    for empresa in empresas:
        funcionario.empresas.remove(empresa)
    funcionario.save()

    for empresa in empresas:
        if 'empresa-'+str(empresa.id) in request.POST: 
            variavel = request.POST['empresa-'+str(empresa.id)]
            funcionario.empresas.add(Empresa.objects.get(id=int(empresa.id)))
    funcionario.save()
    return redirect('listar_funcionarios')

def listar_funcionarios(request):
    if verificaLogin(request) == False:
        return render(request, 'entrar.html')
    if request.session['empresa'] == True:
        return redirect('dashboard')
    if request.method == 'POST':

        funcionario = Funcionario()

        funcionario.nome = request.POST['nome']
        funcionario.cpf = request.POST['cpf']
        funcionario.senha = request.POST['senha']
        funcionario.save()

        loc = Localizacao()
        loc.latitude = '-5.08921'
        loc.longitude = '-42.8016'
        loc.data = '2020-05-30 00:00:00.000000'
        loc.save()
        loc.funcionario = funcionario
        loc.save()

        empresas = Empresa.objects.all()
        for empresa in empresas:
            if 'empresa-'+str(empresa.id) in request.POST: 
                variavel = request.POST['empresa-'+str(empresa.id)]
                funcionario.empresas.add(Empresa.objects.get(id=int(empresa.id)))

        funcionario.save()
        return redirect('listar_funcionarios')
    else:
        funcionarios = Funcionario.objects.filter(ativo=True).all()
        empresas = Empresa.objects.filter(ativo=True).all()
    return render(request, 'funcionarios.html', {'empresas': empresas, 'funcionarios': funcionarios} )

def listar_entregas(request):
    if verificaLogin(request) == False:
        return render(request, 'entrar.html')
    if request.method == 'POST':

        entrega = Entrega()

        entrega.descricao = request.POST['descricao']

        empresa = request.POST.get('empresa')
        if empresa != '0':
            entrega.empresa = Empresa.objects.get(id=int(empresa))

        funcionario = request.POST.get('funcionario')
        if funcionario != '0':
            entrega.funcionario = Funcionario.objects.get(id=int(funcionario))

        entrega.save()

        loc = Localizacao()
        loc.latitude = '-5.08921'
        loc.longitude = '-42.8016'
        loc.data = datetime.now()
        loc.save()
        loc.entrega = entrega
        loc.save()

        return redirect('listar_entregas')
    else:
        funcionarios = Funcionario.objects.filter(ativo=True)
        empresas = Empresa.objects.filter(ativo=True)
        if request.session['empresa'] == True:
            entregas_total = Entrega.objects.filter(ativo=True).order_by('id')
            entregas = []
            for entrega in entregas_total:
                if entrega.empresa.id == request.session['id_empresa']:
                    entregas.append(entrega)
        else:
            entregas = Entrega.objects.filter(ativo=True).order_by('id')
            
    return render(request, 'entregas.html', {'empresas': empresas, 'funcionarios': funcionarios, 'entregas': entregas.reverse()} )

def carga(request):
    return render(request, 'entrar.html')



