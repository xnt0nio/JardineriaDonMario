from django.db import models
from datetime import date
from django.contrib.auth.models import User
from datetime import timedelta

# Create your models here.

# ES DONDE CREAN LAS TABLAS
class TipoProducto(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    descripcion = models.CharField(max_length=250)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    vencimiento = models.DateField(default=date.today)
    imagen = models.ImageField(null=True,blank=True)
    vigente = models.BooleanField()


    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_agregada = models.IntegerField(default=0)

    class Meta:
        db_table = 'db_carrito'


#class HistorialCompra(models.Model):

    #cantidad_agregada = models.IntegerField(default=0)

    #def str(self):
        #return self.nombre_producto        






class Suscripcion(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario.username