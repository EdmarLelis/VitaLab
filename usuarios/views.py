from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.
def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        primeiro_nome = request.POST.get("primeiro_nome")
        ultimo_nome = request.POST.get("ultimo_nome")
        Username = request.POST.get("username")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get("confirmar_senha")

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas devem ser identinticas!')
            return redirect('/usuarios/cadastro')
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve ter no minimo 7 caracteres!')
            return redirect('/usuarios/cadastro')

        try:
            user = User.objects.create_user(
                first_name = primeiro_nome,
                last_name = ultimo_nome,
                username = Username,
                email = email,
                password = senha
            )

        except:
            messages.add_message(request, constants.ERROR, 'Erro interno, contate um administrador.')
            return redirect('/usuarios/cadastro')

        messages.add_message(request, constants.SUCCESS, 'Parabéns! Usuario cadastrado com sucesso.')
        return redirect('/usuarios/login')

def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get("senha")

        user = authenticate(username=username, password=senha)
        
        if user:
            login(request, user)
            return redirect('/')
        else:
            messages.add_message(request, constants.ERROR, 'Usuario ou senha incorretos.')
            return redirect('/usuarios/login')