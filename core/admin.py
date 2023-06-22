from django.contrib import admin
from .models import *
# Register your models here.
#deja en modo tabla la visualizacion en el admin

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre','precio','stock','descripcion','tipo','vigente','vencimiento']
    search_fields = ['nombre']
    list_per_page = 10
    list_filter = ['tipo','precio']
    list_editable = ['precio','stock','descripcion','tipo','vencimiento','vigente']

#class seguimientoAdmin(admin.ModelAdmin):
#    list_display = ['nombre_producto','precio_producto','cantidad_agregada']
#    search_fields = ['nombre_producto']
#    list_per_page = 10
#    list_editable =  ['precio_producto','cantidad_agregada']

admin.site.register(TipoProducto)
admin.site.register(Producto,ProductoAdmin)
#admin.site.register(Seguimiento,seguimientoAdmin)
admin.site.register(Carrito)