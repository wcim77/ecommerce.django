from django.urls import path
from . import views

urlpatterns = [
    path('', views.almacen, name='almacen'),
    path('categoria/<slug:categoria_slug>/', views.almacen, name='productos_por_categoria'),
    path('categoria/<slug:categoria_slug>/<slug:producto_slug>', views.producto_detalle, name='producto_detalle'),
    path('buscar/', views.buscar, name='buscar'),
   
    
]
