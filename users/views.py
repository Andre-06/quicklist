from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as lg
from django.shortcuts import redirect

#verificar se a senha tem mais de 6 digitos
#se tem caracter especial
#se o email é um email

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/posts/new_post')

    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        form = {
            "name": request.POST.get('name'),
            "email": request.POST.get('email'),
            "password": request.POST.get('password'),
            "confirm_password": request.POST.get('confirm_password')
        }
        
        if any([len(form[item].strip()) == 0 for item in form]):
            messages.add_message(request, constants.WARNING, 'Preencha todos os campos corretamente')
            return render(request, 'cadastro.html')
        
        if form['password'] != form['confirm_password']:
            messages.add_message(request, constants.WARNING, 'Digite senhas iguais')
            return render(request, 'cadastro.html')

        try:    
            user = User.objects.create_user(
                username=form['name'],
                email=form['email'],
                password=form['password']
            )

            #mensagem de sucesso
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso')
            return render(request, 'cadastro.html')
        except IntegrityError:
            messages.add_message(request, constants.ERROR, 'Nome de usuário ja cadastrado')
            return render(request, 'cadastro.html')
        except:
            messages.add_message(request, constants.ERROR, 'Ocorreu um erro inesperado, tente novamente mais tarde X_X')
            return render(request, 'cadastro.html')

def logar(request):
    if request.user.is_authenticated:
        return redirect('/posts/new_post')


    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        data = {
            "name": request.POST.get('name'),
            "password": request.POST.get('password'),
        }    
        
        user = authenticate(username=data['name'], password=data['password'])

        if user:
            login(request, user)
            return redirect('/posts/new_post')
        else:
            messages.add_message(request, constants.ERROR, 'Usuários ou senha incorretos')
            return render(request, 'login.html')

def logout(request):
    lg(request)     
    return redirect('/auth/login')
        