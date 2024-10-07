from django.contrib import admin
from .models import Producto, Variacion


# Register your models here.
class ProductoAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':("nombre_producto",)}
    list_display = ('nombre_producto','slug','precio','stock','is_available','created_date','modified_date')
    list_filter = ('is_available','created_date','modified_date')
    list_editable = ('precio','stock','is_available')
    
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Variacion)
