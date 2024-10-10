from django.shortcuts import render
from cuentas.forms import RegisterForm
from cuentas.models import Cuenta

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
            genero=form.cleaned_data['genero']
            username =email.split('@')[0]
            password =form.cleaned_data['password']

            user = Cuenta.objects.create_user(nombre=nombre,apellido=apellido,email=email,username=username,password=password)
            user.fecha_nacimiento = fecha_nacimiento
            user.telefono = telefono
            user.save()
    else:
        form = RegisterForm()   
    context = {
        'form': form,
    }
    return render(request,'cuentas/registroUsuario.html',context)


def login(request):
    return render(request,'cuentas/iniciarSesion.html')


def logout(request):
    return render(request,'cuentas/cerrarSesion.html')
