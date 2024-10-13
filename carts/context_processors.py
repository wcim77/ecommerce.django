from .models import Carrito, CarritoItem
from .views import _carrito_id

def counter(request):
    carrito_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Carrito.objects.filter(carrito_id=_carrito_id(request)).first()  # obtenemos el carrito
            if request.user.is_authenticated:
                carrito_items = CarritoItem.objects.all().filter(user=request.user)
            else:    
                carrito_items = CarritoItem.objects.all().filter(carrito= cart)# obtenemos los items del carrito
            for carrito_item in carrito_items:
                    carrito_count += carrito_item.cantidad  # corregido para acceder a la instancia
        except Carrito.DoesNotExist:
            carrito_count = 0
    return dict(carrito_count=carrito_count)