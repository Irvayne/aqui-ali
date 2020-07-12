
from django.shortcuts import render, redirect
from core.models import Perfil, Empresa, Funcionario, Entrega, Localizacao
from core.carga import realizarCarga


def home(request):
	return render(request, 'index.html')

def entrar(request):
    if request.method == 'POST':
        login = request.POST['login']
        senha = request.POST['senha']
        try:
            perfil = Perfil.objects.get(login = login, senha=senha)
            request.session['login'] = login
            request.session['senha'] = senha
            return redirect('dashboard')
        except:
            try:
                empresa = Empresa.objects.get(cnpj=login, senha=senha)
                return redirect('dashboard')
            except:
                return render(request, 'entrar.html')
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
    return render(request, 'entrar.html')


def dashboard(request):
    if verificaLogin(request) == False:
        return render(request, 'entrar.html')

    funcionarios = Funcionario.objects.all()
    empresas = Empresa.objects.all()

    listaFuncionario = []

    for f in funcionarios:
        fun = {}
        fun["nome"] = f.nome
        for loc in f.localizacoes.all():
            fun["latitude"] = loc.latitude
            fun["longitude"] = loc.longitude
        listaFuncionario.append(fun)



    return render(request, 'dashboard.html' , {'empresas': empresas, 'funcionarios': listaFuncionario})

def listar_empresas(request):
    if verificaLogin(request) == False:
        return render(request, 'entrar.html')
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
        empresas = Empresa.objects.all()
    return render(request, 'empresas.html', {'empresas': empresas} )


def listar_funcionarios(request):
    if verificaLogin(request) == False:
        return render(request, 'entrar.html')
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

        empresa = request.POST.get('empresa')

        if empresa != '0':
            print('selecionou empresa')
            funcionario.empresas.add(Empresa.objects.get(id=int(empresa)))

        funcionario.save()
        return redirect('listar_funcionarios')
    else:
        funcionarios = Funcionario.objects.all()
        empresas = Empresa.objects.all()
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
        return redirect('listar_entregas')
    else:
        funcionarios = Funcionario.objects.all()
        empresas = Empresa.objects.all()
        entregas = Entrega.objects.all()
    return render(request, 'entregas.html', {'empresas': empresas, 'funcionarios': funcionarios, 'entregas': entregas} )

def carga(request):
    realizarCarga()
    return render(request, 'entrar.html')



