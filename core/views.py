from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .serializers import *
from rest_framework import viewsets
import requests

#NOS PERMITE MOSTRAR LA INFO
class ProductoViewsets(viewsets.ModelViewSet):
    queryset = Producto.objects.all()    
    #queryset = Producto.objects.filter()    

    serializer_class = ProductoSerializer

class TipoProductoViewsets(viewsets.ModelViewSet):
    queryset = TipoProducto.objects.all()    
    #queryset = Producto.objects.filter()    

    serializer_class = TipoProductoSerializer    
####

# Create your views here.
def index(request):  
    productosAll = Producto.objects.all() # SELECT * FROM producto
    
    data = {
        'listaProductos' : productosAll
    }
    return render(request, 'core/index.html', data)

def indexapi(request):  
    # obtiene los datoas del api
    respuesta = requests.get('http://127.0.0.1:8000/api/productos/')
    respuesta2 = requests.get('https://mindicador.cl/api')
    respuesta3 = requests.get('https://rickandmortyapi.com/api/character')
    # transformamos el json 
    productos = respuesta.json()
    monedas = respuesta2.json()
    envolvente = respuesta3.json()
    personajes = envolvente['results']

    data = {
        'listaProductos' : productos,
        'monedas' : monedas,
        'personajes' : personajes,
    }
    return render(request, 'core/indexapi.html', data)



# CRUD
@login_required
def add(request):
    data = {
        'form' : ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES) # OBTIENE LA DATA DEL FORMULARIO
        if formulario.is_valid():
            formulario.save() # INSERT INTO.....
            #data['msj'] = "Producto guardado correctamente"
            messages.success(request, "Producto almacenado correctamente")
    return render(request, 'core/add-product.html', data)
@login_required
def update(request, id):
    producto = Producto.objects.get(id=id) # OBTIENE UN PRODUCTO POR EL ID
    data = {
        'form' : ProductoForm(instance=producto) # CARGAMOS EL PRODUCTO EN EL FORMULARIO
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES) # NUEVA INFORMACION
        if formulario.is_valid():
            formulario.save() # INSERT INTO.....
            #data['msj'] = "Producto actualizado correctamente"
            messages.success(request, "Producto modificado correctamente")
            data['form'] = formulario # CARGA LA NUEVA INFOR EN EL FORMULARIO

    return render(request, 'core/update-product.html', data)

@login_required
def delete(request, id):
    producto = Producto.objects.get(id=id) # OBTIENE UN PRODUCTO POR EL ID
    producto.delete()

    return redirect(to="index")

def about(request):
    return render(request, 'core/about.html')

def blog(request):
    return render(request, 'core/blog.html')

def suscripcion(request):
    return render(request, 'core/suscripcion.html')


def pago(request):
    if request.method == 'POST':
        productos_carrito = Carrito.objects.all()

        for producto_carrito in productos_carrito:
            producto = Producto.objects.get(nombre=producto_carrito.nombre_producto)
            cantidad_comprada = producto_carrito.cantidad_agregada
            producto.stock -= cantidad_comprada
            producto.save()

            seguimiento = Seguimiento(
                nombre_producto=producto.nombre,
                precio_producto=producto.precio,
                imagen=producto.imagen,
                cantidad_agregada=cantidad_comprada
            )
            seguimiento.save()

        productos_carrito.delete()

        return redirect('seguimiento')

    return render(request, 'core/pago.html')


 
def checkout(request):
    carrito = Carrito.objects.all()
    respuesta2 = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta2['serie'][0]['valor']
    #total_precio = total_precio/valor_usd
    
    total_precio = sum(item.precio_producto * item.cantidad_agregada for item in carrito)
    total_precio = round(total_precio/valor_usd,2)
    for producto in carrito:
        producto.total_producto = producto.precio_producto * producto.cantidad_agregada
        
    datos = { 
        'listarproductos': carrito, 
        'total_precio' : total_precio
    }
            
    return render(request, 'core/checkout.html', datos)

@login_required
def seguimiento(request):
    seguimientos = Seguimiento.objects.all()

    total_precio = sum(item.precio_producto * item.cantidad_agregada for item in seguimientos)

    for seguimiento in seguimientos:
        seguimiento.total_producto = seguimiento.precio_producto * seguimiento.cantidad_agregada

    datos = {
        'seguimientos': seguimientos,
        'total_precio': total_precio
    }

    return render(request, 'core/seguimiento.html', datos)


##def seguimiento(request):
    seguimientos = Seguimiento.objects.all()
    seguimientos.delete()  # Elimina todos los objetos de la lista

    total_precio = 0

    datos = {
        'seguimientos': [],
        'total_precio': total_precio
    }

    return render(request, 'core/seguimiento.html', datos)


def crear(request):
    return render(request, 'core/crear.html')


def pagosub(request):
    return render(request, 'core/pagosub.html')

def contact(request):
    return render(request, 'core/contact.html')

def shopgrid(request):
    productosAll = Producto.objects.all()
    page = request.GET.get('page', 1) # OBTENEMOS LA VARIABLE DE LA URL, SI NO EXISTE NADA DEVUELVE 1
    
    
    try:
        paginator = Paginator(productosAll, 5)
        productosAll = paginator.page(page)
    except:
        raise Http404

    data = {
        'listado': productosAll,
        'paginator': paginator
    }    
    return render(request, 'core/shop-grid.html', data)





def shopdetails(request,id):
    
    producto = Producto.objects.get(id=id)
    data = {'Productos': producto}

    if request.method == 'POST':
        nombre_producto = request.POST.get('nombre_producto')
        precio_producto = request.POST.get('precio_producto')
        imagen_producto = request.POST.get('imagen_producto')
        cantidad_agregada = int(request.POST.get('producto.cantidad_agregada', 1))

        # Verificar si el producto ya existe en el carrito
        carrito = Carrito.objects.filter(nombre_producto=nombre_producto).first()
        if carrito:
            carrito.cantidad_agregada += cantidad_agregada
            carrito.save()
        else:
            carrito = Carrito(nombre_producto=nombre_producto, precio_producto=precio_producto, imagen=imagen_producto, cantidad_agregada=cantidad_agregada)
            carrito.save()

        messages.success(request, "Producto almacenado correctamente")
    
    return render(request, 'core/shop-details.html', data)
  

def main(request):
    return render(request, 'core/main.html')


#carrito
# shoping es donde se almacena cuando aniadimos al carrito 
def shopingcart(request):
    carrito = Carrito.objects.all()
    total_precio = sum(item.precio_producto * item.cantidad_agregada for item in carrito)

    for item in carrito:
        item.total_producto = item.precio_producto * item.cantidad_agregada

    datos = { 
        'listarproductos': carrito, 
        'total_precio' : total_precio
    }

    return render(request, 'core/shoping-cart.html', datos)


def eliminar_producto(request, id):
    carro = Carrito.objects.get(id=id)
    carro.delete()
    return redirect("shopingcart")
    