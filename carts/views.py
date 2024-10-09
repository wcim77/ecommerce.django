from urllib import request
from django.shortcuts import redirect, render,get_object_or_404

from almacen.models import Producto, Variacion
from carts.models import Carrito, CarritoItem


# Create your views here.
def _carrito_id(request):
    carrito = request.session.session_key
    if not carrito:
        carrito = request.session.create()
    return carrito


    
def add_carrito(request,producto_id):
    producto = Producto.objects.get(id=producto_id) #con esto obtenemos el productos
    producto_variaciones = [] #creamos una lista vacia
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                variacion = Variacion.objects.get(producto=producto,variacion_categoria__iexact=key,valor_variacion__iexact=value)
                producto_variaciones.append(variacion)
            except:
                pass
  
    try:
        cart = Carrito.objects.get(carrito_id=_carrito_id(request)) #con esto obtenemos el carrito
    except Carrito.DoesNotExist:
        cart = Carrito.objects.create(
            carrito_id=_carrito_id(request)
            )
    cart.save()

    try:
        carrito_item = CarritoItem.objects.get(producto=producto,carrito=cart)
        if len (producto_variaciones) > 0:
            carrito_item.variaciones.clear()
            for item in producto_variaciones:
                carrito_item.variaciones.add(item) #si hay variaciones se agregan al item del carrito
        carrito_item.cantidad += 1 #si ya existe el producto en el carrito se le suma uno
        carrito_item.save()
    except CarritoItem.DoesNotExist: 
        carrito_item = CarritoItem.objects.create(
            producto = producto,
            cantidad = 1,
            carrito = cart,
        )
        if len (producto_variaciones) > 0:
            for item in producto_variaciones:
                carrito_item.variaciones.add(item)
        carrito_item.save() #si no existe el producto en el carrito se crea uno nuevo

    return redirect('carritoCompra')


def remove_carrito(request, producto_id):
        carrito = Carrito.objects.get(carrito_id=_carrito_id(request)) #obtenemos el carrito
        producto = get_object_or_404(Producto, id=producto_id) #obtenemos el producto
        try:
            carrito_item = CarritoItem.objects.get(producto=producto, carrito=carrito) #obtenemos el item del carrito
            if carrito_item.cantidad > 1:
                carrito_item.cantidad -= 1
                carrito_item.save()
            else:
                carrito_item.delete() #si la cantidad es 1 se elimina el item
        except CarritoItem.DoesNotExist: #si no existe el item no hacemos nada
            pass
        return redirect('carritoCompra')

def delete_carrito_item(request, producto_id):
        carrito = Carrito.objects.get(carrito_id=_carrito_id(request))  # obtenemos el carrito
        producto = get_object_or_404(Producto, id=producto_id)  # obtenemos el producto
        try:
            carrito_item = CarritoItem.objects.get(producto=producto, carrito=carrito)  # obtenemos el item del carrito
            carrito_item.delete()  # eliminamos el item del carrito
        except CarritoItem.DoesNotExist:  # si no existe el item no hacemos nada
            pass
        return redirect('carritoCompra')

def  carritoCompra(request, total=0, cantidad=0, carrito_items=None):
     try:
        carrito = Carrito.objects.get(carrito_id=_carrito_id(request)) #obtenemos el carrito
        carrito_items = CarritoItem.objects.filter(carrito=carrito, is_active=True) #obtenemos los items del carrito
        for carrito_item in carrito_items: #recorremos los items del carrito
            total += (carrito_item.producto.precio * carrito_item.cantidad) #calculamos el total
            cantidad += carrito_item.cantidad #calculamos el contador
        impuesto = (19 * total)/100 #calculamos el impuesto chileno
        grand_total = total + impuesto #calculamos el total con impuesto
     except Carrito.DoesNotExist: #si no existe el carrito no hacemos nada
        carrito_items = []
        impuesto = 0
        grand_total = 0
        total = 0
        cantidad = 0
      
     context = {
         'carrito_items': carrito_items,
         'total': total,
         'contador': cantidad,
         'impuesto' : impuesto,
         'grand_total': grand_total,

     }  #pasamos los items del carrito, el total y el contador
     return render(request,'almacen/carrito.html',context) #retornamos el template con el contexto

