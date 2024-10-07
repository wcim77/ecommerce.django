from django.urls import path
from . import views

urlpatterns = [
    path('', views.carritoCompra, name='carritoCompra'),
    path('add_carrito/<int:producto_id>/', views.add_carrito, name='add_carrito'), #aqui se le pasa el id del producto
]