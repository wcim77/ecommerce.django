from django.shortcuts import  render
from  almacen.models import Producto

def inicio(request):
    productos = Producto.objects.all().filter(is_available=True)

    context = { 
        'productos':productos,
     }
    return render (request,'inicio.html',context)
