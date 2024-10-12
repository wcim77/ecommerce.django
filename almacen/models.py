from django.db import models
from django.urls import reverse
from categoria.models import Categoria


# Create your models here.
class Producto(models.Model):
    nombre_producto= models.CharField(max_length=200,unique=True)
    slug =models.SlugField(max_length=200,unique=True)
    descripcion = models.TextField(max_length=500,blank=True)
    #precio = models.DecimalField(max_digits=10,decimal_places=2)
    precio = models.PositiveIntegerField()
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



class VariacionManager(models.Manager):
    def modelos(self):
        return super(VariacionManager,self).filter(variacion_categoria='modelo',is_active=True)
    
    def sizes(self):
        return super(VariacionManager,self).filter(variacion_categoria='size',is_active=True)
    

variacion_categoria_choice = (
    ('modelo','modelo'),
    ('size','size'),
)


class Variacion(models.Model):
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    variacion_categoria = models.CharField(max_length=100, choices=variacion_categoria_choice)
    valor_variacion = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date =models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)

    objects = VariacionManager()

    def __str__(self): 
        return self.valor_variacion


