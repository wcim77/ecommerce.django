from django.urls import path
from . import views

urlpatterns = [
    path('', views.almacen, name='almacen'),
    path('<slug:categoria_slug>/', views.almacen, name='productos_por_categoria'),
    path('<slug:categoria_slug>/<slug:producto_slug>', views.producto_detalle, name='producto_detalle'),
]
