import datetime
from django.shortcuts import redirect, render
from django.http import HttpResponse

from carts.models import CarritoItem
from pedidos.forms import PedidoForm
from pedidos.models import pedido


def punto_pago(request):
    return render(request, 'pedidos/punto_pago.html')


def crear_pedido(request, total=0, cantidad=0):
    current_user = request.user

    # Si el carrito del usuario actual tiene items
    carrito_items = CarritoItem.objects.filter(user=current_user)
    carrito_count = carrito_items.count()
    if carrito_count <= 0:
        return redirect('almacen')
    
    impuesto = 0
    grand_total = 0
    for carrito_item in carrito_items:  # Recorremos los items del carrito
        total += (carrito_item.producto.precio * carrito_item.cantidad)  # Calculamos el total
        cantidad += carrito_item.cantidad  # Calculamos el contador
    impuesto = (19 * total) / 100  # Calculamos el impuesto chileno
    grand_total = total + impuesto 

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            try:
                # Creamos una instancia de 'Pedido' y guardamos los datos del formulario
                data = pedido()
                data.user = current_user
                data.nombre = form.cleaned_data['nombre']
                data.apellido = form.cleaned_data['apellido']
                data.telefono = form.cleaned_data['telefono']
                data.email = form.cleaned_data['email']
                data.direccion_linea_1 = form.cleaned_data['direccion_linea_1']
                data.direccion_linea_2 = form.cleaned_data['direccion_linea_2']
                data.ciudad = form.cleaned_data['ciudad']
                data.estado = form.cleaned_data['estado']
                data.pais = form.cleaned_data['pais']
                data.nota_pedido = form.cleaned_data['nota_pedido']
                data.total_pedido = grand_total
                data.impuesto_pedido = impuesto
                data.ip = request.META.get('REMOTE_ADDR')
                data.pago_id = None
                data.save()

                # Generar el número de pedidos
                yr = int(datetime.date.today().strftime('%Y'))
                mt = int(datetime.date.today().strftime('%m'))
                dt = int(datetime.date.today().strftime('%d'))
                d = datetime.date(yr, mt, dt)
                current_date = d.strftime("%Y%m%d")  # 20210715
                numero_orden = current_date + str(data.id)
                data.numero_orden = numero_orden
                data.save()

                pedido_obj = pedido.objects.get(user=current_user, is_ordered=False, numero_orden=numero_orden) # Obtenemos el pedido actual
                context = {
                    'pedido': pedido_obj,
                    'carrito_items': carrito_items,
                    'total': total,
                    'impuesto': impuesto,
                    'grand_total': grand_total,
                }
                return render(request, 'pedidos/punto_pago.html', context) # Redirigimos al punto de pago
            except Exception as e:
                print(f"Error al guardar el pedido: {e}")
        else:  # Si el formulario no es válido, imprimimos los errores en la consola
            print("Formulario no válido")
            print(form.errors)
            return HttpResponse("Formulario no válido")
    
    else:
        form = PedidoForm()  # Si el método no es POST, creamos un formulario vacío
    context = {
        'form': form,
        'carrito_items': carrito_items,
        'total': total,
        'cantidad': cantidad,
        'impuesto': impuesto,
        'grand_total': grand_total,
    }

    return render(request, 'almacen/checkout.html', context)
