import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as lg
from django.shortcuts import redirect
import uuid
from django.contrib.auth import get_user_model
from django.core.mail import send_mail


#verificar se a senha tem mais de 6 digitos
#se tem caracter especial
#se o email é um email

def signup(request):
    if request.user.is_authenticated:
        return redirect('/checklist/you_lists/')

    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        form = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password')
        }

        if any([len(form[item].strip()) == 0 for item in form]):
            messages.add_message(request, constants.WARNING, 'Preencha todos os campos corretamente')
            return render(request, 'signup.html')
        if len(form['password']) < 6:
            messages.add_message(request, constants.WARNING, 'Insira uma senha com mais de seis dígitos')
            return render(request, 'signup.html')
        
        try:    
            id = uuid.uuid4()

            send_mail(
                'Verificação do Email', 
                f'Siga o link: https://127.0.0.1:8000/verify/{id}',
                'quicklistverificatio@gmail.com',
                [form['email']],
                fail_silently=False)

            user = User.objects.create_user(
                username=form['username'],
                email=form['email'],
                password=form['password'],
                verified_code=id
            )

            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso, verifique seu email')
            return render(request, 'verify.html')
        
        except IntegrityError:
            messages.add_message(request, constants.ERROR, 'Email ja cadastrado')
            return render(request, 'signup.html')
        """
        except:
            messages.add_message(request, constants.ERROR, 'Ocorreu um erro inesperado, tente novamente mais tarde X_X')
            return render(request, 'signup.html')  """

"""
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
"""

def logar(request):
    if request.user.is_authenticated:
        return redirect('/checklist/you_lists/')


    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        data = {
            "email": request.POST.get('email'),
            "password": request.POST.get('password'),
        }    
        
        user = authenticate(email=data['email'], password=data['password'])

        if user:
            login(request, user)
            return redirect('/checklist/you_lists/')
        else:
            messages.add_message(request, constants.ERROR, 'Usuários ou senha incorretos')
            return render(request, 'login.html')


def logout(request):
    lg(request)     
    return redirect('/auth/login')

def verify_email(request, verification_code):
    if (datetime.datetime.now() - request.user.registration_date) >= datetime.timedelta(days=1):
        messages.add_message(request, constants.ERROR, 'O tempo de verificação ja expirou')
        return render('sigup/')
    try:
        user = User.objects.get(verified_code = verification_code, email=request.user.email)
        user.is_verified = True
        user.save()
        messages.add_message(request, constants.SUCCESS, "Email verificado com sucesso")
        return redirect('login/')
    except User.DoesNotExists:
        messages.add_message(request, constants.ERROR, "O codigo de verificação é inválido")
        return redirect('signup/')
        