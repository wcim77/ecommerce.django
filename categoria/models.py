from django.db import models
from django.urls import reverse

# Create your models here.

class Categoria(models.Model):
    nombre_categoria=models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    descripcion=models.TextField(max_length=200,blank=True)
    cat_imagen=models.ImageField(upload_to='fotos/categorias',blank=True)

    class Meta:
        verbose_name='Categoria'
        verbose_name_plural='Categorias'
        
    def get_url(self):
            return reverse('productos_por_categoria',args=[self.slug])
    
    def __str__(self):
        return self.nombre_categoria
    