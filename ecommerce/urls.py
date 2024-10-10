
from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.inicio,name='inicio'),
    path('almacen/',include('almacen.urls')),
    path('carts/',include('carts.urls')),
    path('cuentas/',include('cuentas.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
