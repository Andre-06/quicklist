from django.shortcuts import render
from .models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as lg
from django.shortcuts import redirect
from django.utils import timezone
import smtplib
import email.message
from QUICKLIST.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_HOST_PORT


# verificar se a senha tem mais de 6 digitos
# se tem caracter especial
# se o email é um email


def signup(request):
    if request.user.is_authenticated:
        return redirect('/checklist/your_lists/')

    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        form = {
            'username': request.POST.get('username'),
            'name': request.POST.get('name'),
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
            id = "000000"

            email_body = f"""
            <p>Olá {form['username']},</p>
            
            <p>Seu cadastro já foi relalizado, basta somente você verificar seu email</p>
            <p>Para isso, click no botão abaixo</p>

            <a href='http://127.0.0.1:8000/auth/verify/{id}'> VERIFICAR </button>
            """

            msg = email.message.Message()
            msg['Subject'] = "Verificação de Email - Quicklist"
            msg['From'] = EMAIL_HOST_USER
            msg['To'] = form['email']
            password = EMAIL_HOST_PASSWORD
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(email_body)

            s = smtplib.SMTP(EMAIL_HOST_PORT)
            s.starttls()
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
            print('Email enviado')

            User.objects.create_user(
                username=form['username'],
                name=form['name'],
                email=form['email'],
                password=form['password'],
                verified_code=id
            )

            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso, verifique seu email')
            return render(request, 'verify.html')

        except IntegrityError:
            messages.add_message(request, constants.ERROR, 'Email ja cadastrado')
            return render(request, 'signup.html')
        except:
            messages.add_message(request, constants.ERROR, 'Ocorreu um erro inesperado, tente novamente mais tarde X_X')
            return render(request, 'signup.html')


def login_request(request):
    if request.user.is_authenticated:
        return redirect('/checklist/your_lists/')

    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        data = {
            "email": request.POST.get('email'),
            "password": request.POST.get('password'),
        }

        user = authenticate(email=data['email'], password=data['password'])
        if user:
            if not user.is_verified:
                messages.add_message(request, constants.ERROR, 'Usuário não verificado')
                return render(request, 'login.html')
            print(user.email)
            login(request, user)
            return redirect('/checklist/your_lists/')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos')
            return render(request, 'login.html')


def logout(request):
    lg(request)
    return redirect('/auth/login')


def verify_email(request, verification_code):
    try:
        user = User.objects.get(verified_code=verification_code)
    except:
        messages.add_message(request, constants.ERROR, "O codigo de verificação é inválido")
        return render(request, 'signup.html')
    if (timezone.now() - user.registration_date) >= timezone.timedelta(days=1):
        messages.add_message(request, constants.ERROR, 'O tempo de verificação ja expirou')
        return render(request, 'signup.html')
    user.is_verified = True
    user.save()
    messages.add_message(request, constants.SUCCESS, "Email verificado com sucesso")
    return render(request, 'login.html')
