from django.shortcuts import render

# Create your views here.
def registerUser(request):
    return render(request,'cuentas/registroUsuario.html')


def login(request):
    return render(request,'cuentas/iniciarSesion.html')


def logout(request):
    return render(request,'cuentas/cerrarSesion.html')
