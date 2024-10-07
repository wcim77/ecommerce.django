
from django.shortcuts import render, get_object_or_404
from carts.models import CarritoItem
from carts.views import _carrito_id
from categoria.models import Categoria
from .models import Producto
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def almacen(request, categoria_slug=None):
    categorias = None
    productos = None

    if categoria_slug is not None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug) #obtenemos la categoria
        productos = Producto.objects.filter(categoria=categorias, is_available=True)    #obtenemos los productos de la categoria
        producto_count = productos.count() #contamos los productos
        paginator = Paginator(productos, 6)
        page = request.GET.get('page')
        paged_productos = paginator.get_page(page)
        producto_count = productos.count()


    else:
        productos = Producto.objects.all().filter(is_available=True).order_by('id') #obtenemos todos los productos
        paginator = Paginator(productos, 3)
        page = request.GET.get('page')
        paged_productos = paginator.get_page(page)
        producto_count = productos.count()

    context = { 
        'productos':  paged_productos,
        'producto_count': producto_count,
    }

    return render(request, 'almacen/almacen.html', context)

def producto_detalle(request, categoria_slug, producto_slug):
    try:
        single_producto = Producto.objects.get(categoria__slug=categoria_slug, slug=producto_slug)
        in_carrito =CarritoItem.objects.filter(carrito__carrito_id=_carrito_id(request),producto=single_producto).exists() #verificamos si el producto esta en el carrito
    except Exception as e:
        raise e
    context = {
        'single_producto': single_producto,
        'in_carrito': in_carrito,
    }
    return render(request, 'almacen/producto_detalle.html', context)
