from django.contrib import admin
from .models import pagos, pedido, pedido_producto
# Register your models here.

admin.site.register(pagos)
admin.site.register(pedido)
admin.site.register(pedido_producto)
