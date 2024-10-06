from django.db import models
from django.urls import reverse
from categoria.models import Categoria


# Create your models here.
class Producto(models.Model):
    nombre_producto= models.CharField(max_length=200,unique=True)
    slug =models.SlugField(max_length=200,unique=True)
    descripcion = models.TextField(max_length=500,blank=True)
    precio = models.DecimalField(max_digits=10,decimal_places=2)
    imagen = models.ImageField(upload_to='fotos/productos',blank=True)
    stock =models.IntegerField()
    is_available = models.BooleanField(default=True)
    categoria = models.ForeignKey('categoria.Categoria',on_delete=models.CASCADE)
    created_date =models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('producto_detalle',args=[self.categoria.slug,self.slug])

    def __str__(self):
        return self.nombre_producto
    

