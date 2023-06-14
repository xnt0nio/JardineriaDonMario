from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from .serializers import *
from rest_framework import viewsets
import requests
from django.contrib.auth import authenticate, login
from datetime import date




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
@permission_required('core.add-product')
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
@permission_required('core.update-product')
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

@permission_required('core.delete')
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

def vaciar_carrito(request):
    productos_carrito = Carrito.objects.filter()

    # Actualiza el stock de cada producto en base a la cantidad del carrito
    for producto_carrito in productos_carrito:
        producto = producto_carrito.producto
        cantidad_agregada = producto_carrito.cantidad_agregada

        # Resta la cantidad del carrito al stock del producto
        producto.stock -= cantidad_agregada
        producto.save()

    # Elimina todos los registros del carrito del usuario actual
    productos_carrito.delete()

    return redirect('index')  # Redireccionar a la página de inicio después de vaciar el carrito
 


def checkout(request):
    carrito = Carrito.objects.all()
    respuesta2 = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta2['serie'][0]['valor']
    total_precio = sum(item.producto.precio * item.cantidad_agregada for item in carrito)
    total_precio = round(total_precio/valor_usd,2)
    for item in carrito:
        item.total_producto = item.producto.precio * item.cantidad_agregada

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


"""def seguimiento(request):
    seguimientos = Seguimiento.objects.all()
    seguimientos.delete()  # Elimina todos los objetos de la lista

    total_precio = 0

    datos = {
        'seguimientos': [],
        'total_precio': total_precio
    }

    return render(request, 'core/seguimiento.html', datos)"""


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





"""def shopdetails(request,id):
    
    producto = Producto.objects.get(id=id)
    data = {'Productos': producto}

    if request.method == 'POST':
        tipo = TipoProducto()
        tipo.tipo = request.POST.get('tipo')
        producto2 = Producto()
        producto2.id = producto.id
        producto2.nombre = request.POST.get('nombre')
        producto2.precio = request.POST.get('precio')
        producto2.stock = request.POST.get('stock')
        producto2.descripcion = request.POST.get('descripcion')
        producto2.tipo = tipo
        producto2.vencimiento = request.POST.get('vencimiento')
        producto2.imagen = request.POST.get('imagen')
        producto2.vigente = request.POST.get('vigente')
        producto2.cantidad_agregada = int(request.POST.get('cantidad_agregada', 1))
        carrito = Carrito()
        carrito.producto_id = producto2.id
        carrito.save()
        messages.success(request, "Producto almacenado correctamente")
    
    return render(request, 'core/shop-details.html', data)"""

def shopdetails(request, id):
    producto = Producto.objects.get(id=id)
    data = {'Productos': producto}

    if request.method == 'POST':
        carrito, created = Carrito.objects.get_or_create(producto=producto)
        cantidad_agregada = int(request.POST.get('cantidad_agregada', 1))
        if not created:
            carrito.cantidad_agregada += cantidad_agregada
        else:
            carrito.cantidad_agregada = cantidad_agregada
        carrito.save()
        messages.success(request, "Producto almacenado correctamente")

    return render(request, 'core/shop-details.html', data)

  

def main(request):
    return render(request, 'core/main.html')


#carrito
# shoping es donde se almacena cuando aniadimos al carrito 
def shopingcart(request):
    carrito = Carrito.objects.all()
    total_precio = sum(item.producto.precio * item.cantidad_agregada for item in carrito)

    for item in carrito:
        item.total_producto = item.producto.precio * item.cantidad_agregada

    datos = { 
        'listarproductos': carrito, 
        'total_precio' : total_precio
    }

    return render(request, 'core/shoping-cart.html', datos)



def eliminar_producto(request, id):
    carro = Carrito.objects.get(id=id)
    carro.delete()
    return redirect("shopingcart")
    
def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            #redirigir al home
            return redirect(to="index")
        data["form"] = formulario    
    return render(request, 'registration/registro.html',data)







@login_required
def purchase_membership(request):
    subscription_success = False

    if request.method == 'POST':
        form = PurchaseMembershipForm(request.POST)
        if form.is_valid():
            membership_id = 123  # Define el ID de la membresía manualmente
            membership = Membership.objects.get(id=membership_id)  # Obtiene la membresía según el ID
            user = request.user

            # Verificar si el usuario ya tiene una suscripción activa
            if Subscription.objects.filter(user=user).exists():
                messages.warning(request, "Ya tienes una suscripción activa.")
                return redirect('purchase_membership')

            # Calcular la fecha de finalización de la suscripción (1 mes a partir de hoy)
            end_date = date.today().replace(day=1)
            end_date = end_date.replace(month=(end_date.month + 1) % 12)
            if end_date.month == 1:
                end_date = end_date.replace(year=end_date.year + 1)

            # Crear una nueva suscripción para el usuario
            subscription = Subscription(user=user, membership=membership, end_date=end_date)
            subscription.save()

            # Actualizar la variable para indicar el éxito de la suscripción
            subscription_success = True
            messages.success(request, "¡Suscripción realizada con éxito!")
            return redirect('index')  # Redirigir nuevamente a la página de inicio

    else:
        form = PurchaseMembershipForm()

    return render(request, 'purchase_membership.html', {'form': form, 'subscription_success': subscription_success})




@login_required
def cancel_subscription(request):
    user = request.user

    # Verificar si el usuario tiene una suscripción activa
    if Subscription.objects.filter(user=user).exists():
        # Obtener la suscripción del usuario
        subscription = Subscription.objects.get(user=user)

        # Eliminar la suscripción
        subscription.delete()

    # Redirigir a una página de confirmación o mostrar un mensaje de éxito
    return redirect('subscription_cancelled')
