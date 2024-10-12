
from django.shortcuts import render, get_object_or_404
from carts.models import CarritoItem
from carts.views import _carrito_id
from categoria.models import Categoria
from .models import Producto
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.core.cache import cache


def almacen(request, categoria_slug=None):
    categorias = None
    productos = None

    if categoria_slug is not None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug) #obtenemos la categoria
        productos = Producto.objects.filter(categoria=categorias, is_available=True).order_by('id')    #obtenemos los productos de la categoria
        producto_count = productos.count() #contamos los productos
        paginator = Paginator(productos, 3)
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

def producto_detalle(request, categoria_slug, producto_slug): #funcion para ver los detalles de un producto
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

def buscar(request):
    productos = Producto.objects.none()  # Inicializa productos como un QuerySet vacío
    categoria = Categoria.objects.all()  # obtenemos todas las categorias
    if 'keyword' in request.GET:         # si se envia una palabra clave
        keyword = request.GET['keyword'] # obtenemos la palabra clave
        if keyword:
            productos = Producto.objects.order_by('-created_date').filter(
                Q(descripcion__icontains=keyword) | Q(nombre_producto__icontains=keyword)
            )  # buscamos los productos que contengan la palabra clave
            categoria = Categoria.objects.all()
            if productos.exists():
                cache.clear()  # borra el cache si se encuentran productos

    context = {
        'productos': productos,
        'categorias': categoria,
        'producto_count': productos.count(),
    }
    return render(request, 'almacen/almacen.html', context)