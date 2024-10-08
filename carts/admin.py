from django.contrib import admin
from.models import Carrito, CarritoItem

# Register your models here.

class CarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito_id','date_added')
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('producto', 'carrito', 'cantidad', 'is_active',)
    list_editable = ('is_active',)
    list_per_page = 10
    list_filter = ('producto', 'carrito', 'is_active','variaciones')


  
admin.site.register(Carrito,CarritoAdmin)
admin.site.register(CarritoItem,CarritoItemAdmin)

