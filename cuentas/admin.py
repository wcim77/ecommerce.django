from django.contrib import admin
from .models import Cuenta
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CuentaAdmin(UserAdmin):
    list_display=('email','nombre','apellido','username','last_login','date_joined','is_active')
    list_display_link =('email','nombre','apellido')
    readonly_fields=('last_login','date_joined')
    ordering = ('-date_joined',)

    filter_horizontal=()
    list_filter=()
    fieldsets=()

admin.site.register(Cuenta,CuentaAdmin) 

