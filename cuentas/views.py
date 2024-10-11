from enum import auto
from venv import logger
from django.contrib import messages
from django.shortcuts import redirect, render
from cuentas.forms import RegisterForm
from cuentas.models import Cuenta
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

#verificacion de correo
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            nombre =form.cleaned_data['nombre']
            apellido =form.cleaned_data['apellido']
            telefono =form.cleaned_data['telefono']
            fecha_nacimiento =form.cleaned_data['fecha_nacimiento']
            email =form.cleaned_data['email']
            username =email.split('@')[0]
            password =form.cleaned_data['password']
            user = Cuenta.objects.create_user(nombre=nombre,apellido=apellido,email=email,username=username,password=password)
            user.fecha_nacimiento = fecha_nacimiento
            user.telefono = telefono
            user.save()
            #activacion de usuario
            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta'
            message = render_to_string('cuentas/cuenta_verificacion_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/cuentas/login/?command=verification&email='+email)
    else:
        form = RegisterForm()   
    context = {
        'form': form,
    }
    return render(request,'cuentas/registroUsuario.html',context)


def login(request): #login
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate( email=email, password=password)

        if user is not None:
            auth.login (request, user)
            #messages.error(request,'El correo o la contraseña son incorrectos')
            return redirect('inicio')
        else:   
            messages.error(request,'El correo o la contraseña son incorrectos')
            return redirect('login')
    return render(request,'cuentas/iniciarSesion.html')


      
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'Ha cerrado sesión correctamente')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Cuenta._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Cuenta.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'La cuenta ha sido activada correctamente.')
        return redirect('login')
    else:
        messages.error(request, 'El enlace de activación es inválido.')
        return redirect('registerUser')
    
@login_required(login_url='login')    
def panel(request):
    return render(request,'cuentas/panel.html')
