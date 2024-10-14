from django.db import models
from almacen.models import Producto, Variacion, Categoria
from cuentas.models import Cuenta

# Create your models here.

class pagos(models.Model):
    user = models.ForeignKey('cuentas.Cuenta', on_delete=models.CASCADE)
    pago_id = models.CharField(max_length=100)
    metodo_pago= models.CharField(max_length=100)
    cantidad_pago=models.IntegerField()
    estado_pago=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.pago_id
    

class pedido(models.Model):

        STATUS = (
             ('Nuevo','Nuevo'),
            ('Pendiente','Pendiente'),
            ('Enviado','Enviado'),
            ('Entregado','Entregado'),
            ('Cancelado','Cancelado'),
        )
        user = models.ForeignKey(Cuenta, on_delete=models.SET_NULL, null=True)
        pago_id = models.ForeignKey(pagos, on_delete=models.SET_NULL, blank=True,null=True)
        numero_orden = models.CharField(max_length=100)
        nombre = models.CharField(max_length=100)
        apellido = models.CharField(max_length=100)
        telefono= models.CharField(max_length=14)
        email = models.EmailField()
        direccion_linea_1 = models.CharField(max_length=100)
        direccion_linea_2 = models.CharField(max_length=100,blank=True)
        pais = models.CharField(max_length=50)
        ciudad = models.CharField(max_length=50)
        estado = models.CharField(max_length=50)
        nota_pedido = models.CharField(max_length=100,blank=True,null=True)
        total_pedido= models.FloatField()
        impuesto_pedido = models.FloatField()
        status = models.CharField(max_length=100,choices=STATUS,default='Nuevo')
        ip = models.CharField(max_length=20,blank=True)
        is_ordered = models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)


        def full_nombre(self):
            return f'{self.nombre} {self.apellido}'
        
        def full_direccion(self):
            return f'{self.direccion_linea_1} {self.direccion_linea_2}'
        
        def __str__(self):
            return self.user.nombre
        
class pedido_producto(models.Model):
    pedido_id = models.ForeignKey(pedido, on_delete=models.CASCADE)
    pago_id = models.ForeignKey(pagos, on_delete=models.SET_NULL, blank=True,null=True)
    user = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variacion = models.ForeignKey(Variacion, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    precio_producto = models.FloatField()
    ordenada = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.producto_id.nombre_producto



