from django.shortcuts import render, get_object_or_404
from categoria.models import Categoria
from .models import Producto

def almacen(request, categoria_slug=None):
    categorias = None
    productos = None

    if categoria_slug is not None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        productos = Producto.objects.filter(categoria=categorias, is_available=True)
        producto_count = productos.count()
    else:
        productos = Producto.objects.all().filter(is_available=True)
        producto_count = productos.count()

    context = { 
        'productos': productos,
        'producto_count': producto_count,
    }

    return render(request, 'almacen/almacen.html', context)

def producto_detalle(request, categoria_slug, producto_slug):
    try:
        single_producto = Producto.objects.get(categoria__slug=categoria_slug, slug=producto_slug)
    except Exception as e:
        raise e
    context = {
        'single_producto': single_producto,
    }
    return render(request, 'almacen/producto_detalle.html', context)
