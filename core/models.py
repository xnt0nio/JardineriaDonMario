from django.db import models
from datetime import date


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
    nombre_producto = models.CharField(max_length=50)
    precio_producto = models.IntegerField()
    imagen = models.ImageField(upload_to="carrito", null=True)
    cantidad_agregada = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre_producto
    
    class Meta:
        db_table = 'db_carrito'


class Seguimiento(models.Model):
    nombre_producto = models.CharField(max_length=50)
    precio_producto = models.IntegerField()
    imagen = models.ImageField(upload_to="seguimiento", null=True)
    cantidad_agregada = models.IntegerField(default=0)

    def str(self):
        return self.nombre_producto        