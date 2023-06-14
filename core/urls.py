from django import views
from django.urls import path, include
from .views import *
from rest_framework import routers

#Creamos las rutas del api
router = routers.DefaultRouter()
router.register('productos', ProductoViewsets)
router.register('tipoproductos', TipoProductoViewsets)


urlpatterns = [
    #api
    path('api/', include(router.urls)),

    #rutas
    path('', index, name="index"),
    path('indexapi', indexapi, name="indexapi"),
    path('blog/', blog, name="blog"),
    path('shopingcart/', shopingcart, name="shopingcart"),
    path('checkout/', checkout, name="checkout"),
    path('contact/', contact, name="contact"),
    path('shopgrid/', shopgrid, name="shopgrid"),
    path('shopdetails/<id>/', shopdetails, name="shopdetails"),
    path('seguimiento/', seguimiento, name="seguimiento"),
    path('crear/', crear, name="crear"),
    path('pago/', pago, name="pago"),
    path('pagosub/', pagosub, name="pagosub"),
    path('suscripcion/', suscripcion, name="suscripcion"),
    path('main/', main, name="main"),
    #CRUD
    path('add/', add, name="add"),
    path('update/<id>/', update, name="update"),
    path('delete/<id>/', delete, name="delete"),
    path('eliminar_producto/<id>/', eliminar_producto, name="eliminar_producto"),
    path('vaciar_carrito/', vaciar_carrito, name='vaciar_carrito'),
    path('registro/', registro, name='registro'),
    
]