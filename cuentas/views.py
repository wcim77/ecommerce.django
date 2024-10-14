from enum import auto
from venv import logger
from django.contrib import messages
from django.shortcuts import redirect, render
from carts.models import Carrito, CarritoItem
from carts.views import _carrito_id
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

import requests

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
            try:
                carrito = Carrito.objects.get(carrito_id=_carrito_id(request))
                is_carrito_item_exists = CarritoItem.objects.filter(carrito=carrito).exists()
                if is_carrito_item_exists:
                    carrito_item = CarritoItem.objects.filter(carrito=carrito)

                    #obtenemos los items del carrito del usuario
                    producto_variacion = []
                    for item in carrito_item:
                        variacion = item.variaciones.all()
                        producto_variacion.append(list(variacion))
                    #obtenemos los items del carrito del usuario
                    if is_carrito_item_exists:
                        carrito_item = CarritoItem.objects.filter(user=user)
                        ex_var_list=[]
                        id = []
                        for item in carrito_item:
                            existing_variacion= item.variaciones.all()
                            ex_var_list.append(list(existing_variacion))
                            id.append(item.id)
                        for pr in producto_variacion:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CarritoItem.objects.get(id=item_id)
                                item.cantidad += 1
                                item.user = user
                                item.save()
                            else:
                                carrito_item = CarritoItem.objects.filter(carrito=carrito)
                                for item in carrito_item:
                                    item.user = user
                                    item.save()
            except:
                pass
            auth.login (request, user)
            messages.success(request,'Ya ha iniciado sesion.')
            url= request.META.get('HTTP_REFERER') #obtenemos la url de la pagina anterior
            try:
                query = requests.utils.urlparse(url).query
                
                #next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&')) #next=/cart/checkout/
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage) 
            except:
                return redirect('panel')      
        else:   
            messages.error(request,'El correo o la contraseña son incorrectos.')
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

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Cuenta.objects.filter(email=email).exists():
            user = Cuenta.objects.get(email__exact=email)

            #reset password
            current_site = get_current_site(request)
            mail_subject = 'Restablecer contraseña'
            message = render_to_string('cuentas/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])  
            send_email.send()

            messages.success(request,'El enlace de restablecimiento de contraseña ha sido enviado a su correo.')
            return redirect('login')    
        else:
            messages.error(request, 'La cuenta no está registrado.')
            return redirect('forgotPassword')
    return render(request,'cuentas/olvidoContrasena.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Cuenta._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Cuenta.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Por favor, restablezca su contraseña.')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Este enlace ha caducado.')
        return redirect('login')
    
def resetPassword(request):
    if request.method =='POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Cuenta.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'La contraseña ha sido restablecida.')
            return redirect('login')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('resetPassword')
    else: 
        return render(request,'cuentas/resetPassword.html')