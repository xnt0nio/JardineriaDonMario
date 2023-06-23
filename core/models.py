from django.db import models
from datetime import date
from django.contrib.auth.models import User


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
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_agregada = models.IntegerField(default=0)

    class Meta:
        db_table = 'db_carrito'

class HistorialCompra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    fecha_compra = models.DateTimeField(auto_now_add=True)

      
class Suscripcion(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario.username
    

class Pedido(models.Model):
    ESTADO_CHOICES = (
        ('validacion', 'Validación'),
        ('preparacion', 'Preparación'),
        ('reparto', 'Reparto'),
        ('entregado', 'Entregado'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    fecha_entrega = models.DateField(null=True)
    nombre_completo = models.CharField(max_length=100, blank=True)
    cantidad = models.IntegerField(default=0, null=True)
    region = models.CharField(max_length=100, blank=True)
    comuna = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    nro_casa_departamento = models.CharField(max_length=50, blank=True)
    celular = models.CharField(max_length=100, blank=True)
    correo = models.CharField(max_length=100, blank=True)
    comentario = models.TextField(blank=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='validacion')

    def str(self):
        return f"Pedido #{self.pk} - {self.usuario.username}"    