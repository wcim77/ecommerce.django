from django.urls import path
from . import views

urlpatterns = [
    path('', views.carritoCompra, name='carritoCompra'),
    path('add_carrito/<int:producto_id>/', views.add_carrito, name='add_carrito'), #aqui se le pasa el id del producto
    path('remove/<int:producto_id>/<int:carrito_item_id>/', views.remove_carrito, name='remove_carrito'), #aqui se le pasa el id del producto
    path('delete/<int:producto_id>/<int:carrito_item_id>/', views.delete_carrito_item, name='delete_carrito_item'), #aqui se le pasa el id del producto
   
   path('checkout/', views.checkout, name='checkout'),
]