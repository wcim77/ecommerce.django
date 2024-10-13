from django.db import models

from almacen.models import Producto, Variacion
from cuentas.models import Cuenta

# Create your models here.

class Carrito(models.Model):
    carrito_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)
 
    def __str__(self):
        return self.carrito_id
    

class CarritoItem(models.Model):
    user = models.ForeignKey(Cuenta,on_delete=models.CASCADE,null=True)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    variaciones = models.ManyToManyField(Variacion, blank=True)
    carrito= models.ForeignKey(Carrito,on_delete=models.CASCADE,null=True)
    cantidad = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.producto.precio * self.cantidad
    
    def __unicode__(self):
        return self.producto
  
    
  
    