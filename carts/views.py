from urllib import request
from django.shortcuts import redirect, render,get_object_or_404

from almacen.models import Producto, Variacion
from carts.models import Carrito, CarritoItem
from django.contrib.auth.decorators import login_required

# Create your views here.
def _carrito_id(request):
    carrito = request.session.session_key
    if not carrito:
        carrito = request.session.create()
    return carrito
#Agregar al carrito  
def add_carrito(request,producto_id):
    current_user = request.user #obtenemos el usuario actual
    producto = Producto.objects.get(id=producto_id) #con esto obtenemos el productos
    if current_user.is_authenticated:  # si el usuario está autenticado      
        producto_variacion = [] #creamos una lista vacia
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variacion = Variacion.objects.get(producto=producto,variacion_categoria__iexact=key,valor_variacion__iexact=value)
                    producto_variacion.append(variacion)
                except:
                    pass
        #creamos una variable para verificar si el producto ya esta en el carrito
        is_carrito_item_exists = CarritoItem.objects.filter(producto=producto,user=current_user).exists() #verificamos si el producto ya esta en el carrito
        if is_carrito_item_exists:
            carrito_item = CarritoItem.objects.filter(producto=producto,user=current_user)
            #recorremos los items del carrito
            #si el producto ya esta en el carrito aumentamos la cantidad
            #si el producto ya esta en el carrito pero con variaciones diferentes
            ex_var_list=[]
            id = []
            #recorremos los items del carrito
            for item in carrito_item:
                existing_variacion= item.variaciones.all()
                ex_var_list.append(list(existing_variacion))
                id.append(item.id)
            #si el producto ya esta en el carrito aumentamos la cantidad
            if producto_variacion in ex_var_list:
                #aumentamos la cantidad
                index=ex_var_list.index(producto_variacion)
                item_id= id[index]
                item = CarritoItem.objects.get(producto=producto,id=item_id)
                item.cantidad += 1
                item.save()
            #si el producto ya esta en el carrito pero con variaciones diferentes
            else:
                carrito_item = CarritoItem.objects.create(
                    producto=producto,
                    cantidad=1,
                    user=current_user,
                )
                if len (producto_variacion) > 0:
                    carrito_item.variaciones.clear()
                    for variacion in producto_variacion:
                        carrito_item.variaciones.add(variacion) #si hay variaciones se agregan al item del carrito
                carrito_item.save()
        else:
            carrito_item = CarritoItem.objects.create(
                producto = producto,
                cantidad = 1,
                user = current_user,
            )
            if len (producto_variacion) > 0:
                carrito_item.variaciones.clear()
                for variacion in producto_variacion:
                    carrito_item.variaciones.add(variacion)
            carrito_item.save() #si no existe el producto en el carrito se crea uno nuevo
        return redirect('carritoCompra')
    
    #si el usuario no esta autenticado
    else: 
        producto_variacion = [] #creamos una lista vacia
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variacion = Variacion.objects.get(producto=producto,variacion_categoria__iexact=key,valor_variacion__iexact=value)
                    producto_variacion.append(variacion)
                except:
                    pass
    
        try:
            cart = Carrito.objects.get(carrito_id=_carrito_id(request)) #con esto obtenemos el carrito
        except Carrito.DoesNotExist:
            cart = Carrito.objects.create(
                carrito_id=_carrito_id(request)
                )
        cart.save()
        #creamos una variable para verificar si el producto ya esta en el carrito
        is_carrito_item_exists = CarritoItem.objects.filter(producto=producto,carrito=cart).exists() #verificamos si el producto ya esta en el carrito
        if is_carrito_item_exists:
            carrito_item = CarritoItem.objects.filter(producto=producto,carrito=cart)
            ex_var_list=[]
            id = []
            #recorremos los items del carrito
            for item in carrito_item:
                existing_variacion= item.variaciones.all()
                ex_var_list.append(list(existing_variacion))
                id.append(item.id)

            print(ex_var_list)    
            #si el producto ya esta en el carrito aumentamos la cantidad
            if producto_variacion in ex_var_list:
                #aumentamos la cantidad
                index=ex_var_list.index(producto_variacion)
                item_id= id[index]
                item = CarritoItem.objects.get(producto=producto,id=item_id)
                item.cantidad += 1
                item.save()
            #si el producto ya esta en el carrito pero con variaciones diferentes
            else:
                carrito_item = CarritoItem.objects.create(
                    producto=producto,
                    cantidad=1,
                    carrito=cart,
                )
                if len (producto_variacion) > 0:
                    carrito_item.variaciones.clear()
                    for variacion in producto_variacion:
                        carrito_item.variaciones.add(variacion) #si hay variaciones se agregan al item del carrito
                carrito_item.save()
        else:
            carrito_item = CarritoItem.objects.create(
                producto = producto,
                cantidad = 1,
                carrito = cart,
            )
            if len (producto_variacion) > 0:
                carrito_item.variaciones.clear()
                for variacion in producto_variacion:
                    carrito_item.variaciones.add(variacion)
            carrito_item.save() #si no existe el producto en el carrito se crea uno nuevo
        return redirect('carritoCompra')

#Borrar del carrito
def remove_carrito(request, producto_id,carrito_item_id):
         #obtenemos el carrito
        producto = get_object_or_404(Producto, id=producto_id) #obtenemos el producto
        try:
            if request.user.is_authenticated: #si el usuario esta autenticado
                carrito_item = CarritoItem.objects.get(producto=producto, user=request.user,id=carrito_item_id) #obtenemos el item del carrito
            else: 
                carrito = Carrito.objects.get(carrito_id=_carrito_id(request))
                carrito_item = CarritoItem.objects.get(producto=producto, carrito=carrito,id=carrito_item_id) #obtenemos el item del carrito
            if carrito_item.cantidad > 1:
                carrito_item.cantidad -= 1
                carrito_item.save()
            else:
                carrito_item.delete() #si la cantidad es 1 se elimina el item
        except CarritoItem.DoesNotExist: #si no existe el item no hacemos nada
            pass
        return redirect('carritoCompra')

#Eliminar del carrito
def delete_carrito_item(request, producto_id,carrito_item_id):
       # obtenemos el carrito
        producto = get_object_or_404(Producto, id=producto_id)  # obtenemos el producto
        if request.user.is_authenticated:  # si el usuario esta autenticado
            carrito_item = CarritoItem.objects.get(producto=producto, user=request.user,id=carrito_item_id)
        else:
            carrito = Carrito.objects.get(carrito_id=_carrito_id(request)) 
            carrito_item = CarritoItem.objects.get(producto=producto, carrito=carrito,id=carrito_item_id)  # obtenemos el item del carrito
        carrito_item.delete()  # eliminamos el item del carrito
        return redirect('carritoCompra')

#Vista del carrito
def  carritoCompra(request, total=0, cantidad=0, carrito_items=None):
     try:
        if request.user.is_authenticated: #si el usuario esta autenticado 
            carrito_items = CarritoItem.objects.filter(user=request.user, is_active=True)
        else:  
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


#Vista de checkout
@login_required(login_url='login')
def checkout(request,total=0, cantidad=0, carrito_items=None):
    try:
        if request.user.is_authenticated: #si el usuario esta autenticado 
            carrito_items = CarritoItem.objects.filter(user=request.user, is_active=True)
        else:  
            carrito = Carrito.objects.get(carrito_id=_carrito_id(request)) #obtenemos el carrito
            carrito_items = CarritoItem.objects.filter(carrito=carrito, is_active=True)
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

     } 
    return render(request,'almacen/checkout.html',context) #retornamos el template de checkout


