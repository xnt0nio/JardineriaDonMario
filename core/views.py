import datetime
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
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import Group
from datetime import datetime





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
    productos_carrito = Carrito.objects.filter(usuario=request.user)
    productos_carrito.delete()

    return redirect('index')  # Redireccionar a la página de inicio después de vaciar el carrito

 
from decimal import Decimal







def checkout(request):
    if request.method == 'POST':
        carrito = Carrito.objects.all()
        respuesta2 = requests.get('https://mindicador.cl/api/dolar').json()
        valor_usd = respuesta2['serie'][0]['valor']
        total_precio = Decimal(str(sum(item.producto.precio * item.cantidad_agregada for item in carrito)))
        total_en_dolar = round(total_precio / Decimal(str(valor_usd)), 2)

        # Definir valores predeterminados para descuento y total_dolares
        descuento = Decimal('0.0')
        total_con_descuento = total_precio
        total_dolares = Decimal('0.0')

        # Verificar si el usuario está suscrito
        if hasattr(request.user, 'suscripcion'):
            descuento_porcentaje = Decimal('0.1')  # 10% de descuento para usuarios suscritos
            descuento = round(total_precio * descuento_porcentaje)
            total_con_descuento = round(total_precio - descuento)
            total_dolares = round(total_con_descuento / Decimal(str(valor_usd)), 2)

        total = total_dolares or total_en_dolar

        fecha_entrega = datetime.now().date() + timedelta(days=5)
        fecha_compra =  datetime.today()
        for item in carrito:
            item.total_producto = item.producto.precio * item.cantidad_agregada
            item.save()  # Guardar los cambios en el modelo Carrito

            HistorialCompra.objects.create(
                usuario=request.user,
                producto=item.producto,
                cantidad=item.cantidad_agregada,
                fecha_compra=fecha_compra
            )

        nombre_completo = request.POST.get('nombre_completo')
        region = request.POST.get('region')
        comuna = request.POST.get('comuna')
        direccion = request.POST.get('direccion')
        nro_casa_departamento = request.POST.get('nro_casa_departamento')
        celular = request.POST.get('celular')
        correo = request.POST.get('correo')
        comentario = request.POST.get('comentario')

        Pedido.objects.create(
            usuario=request.user,
            producto=item.producto,
            cantidad=item.cantidad_agregada,
            nombre_completo=nombre_completo,
            region=region,
            comuna=comuna,
            direccion=direccion,
            nro_casa_departamento=nro_casa_departamento,
            celular=celular,
            correo=correo,
            comentario=comentario,
            fecha_entrega=fecha_entrega
        )

        datos = {
            'listarproductos': carrito,
            'total_precio': total_precio,
            'descuento': descuento,
            'total_con_descuento': total_con_descuento,
            'total_dolares': total_dolares,
            'total_en_dolar': total_en_dolar,
            'total': total,
            'suscrito': hasattr(request.user, 'suscripcion')
        }
        return render(request, 'core/checkout.html', datos)

    else:
        # Código para la solicitud GET (cuando se carga la página)
        carrito = Carrito.objects.all()
        total_precio = Decimal('0')
        
        for item in carrito:
            item.total_producto = item.producto.precio * item.cantidad_agregada
            total_precio += item.total_producto
        
        respuesta2 = requests.get('https://mindicador.cl/api/dolar').json()
        valor_usd = respuesta2['serie'][0]['valor']
        total_en_dolar = round(total_precio / Decimal(str(valor_usd)), 2)

        descuento = Decimal('0.0')
        total_con_descuento = total_precio
        total_dolares = Decimal('0.0')

        if hasattr(request.user, 'suscripcion'):
            descuento_porcentaje = Decimal('0.1')
            descuento = round(total_precio * descuento_porcentaje)
            total_con_descuento = round(total_precio - descuento)
            total_dolares = round(total_con_descuento / Decimal(str(valor_usd)), 2)

        total = total_dolares or total_en_dolar

        datos = {
            'listarproductos': carrito,
            'total_precio': total_precio,
            'descuento': descuento,
            'total_con_descuento': total_con_descuento,
            'total_dolares': total_dolares,
            'total_en_dolar': total_en_dolar,
            'total': total,
            'suscrito': hasattr(request.user, 'suscripcion')
        }
        return render(request, 'core/checkout.html', datos)
















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
@login_required
def historial(request):
    historial_compras = HistorialCompra.objects.filter(usuario=request.user)

    for compra in historial_compras:
        compra.total_productos = compra.producto.precio * compra.cantidad

    datos = {
        'historial_compras': historial_compras
    }
    return render(request, 'core/historial.html', datos)



def shopdetails(request, id):
    producto = Producto.objects.get(id=id)

    if request.method == 'POST':
        cantidad_agregada = int(request.POST.get('cantidad_agregada', 1))

        # Verificar si hay suficiente stock disponible
        if producto.stock >= cantidad_agregada:
            # Obtener el carrito del usuario actual
            carrito, created = Carrito.objects.get_or_create(usuario=request.user, producto=producto)

            # Actualizar la cantidad agregada en el carrito
            carrito.cantidad_agregada += cantidad_agregada
            carrito.save()

            # Restar la cantidad del carrito al stock del producto
            producto.stock -= cantidad_agregada
            producto.save()
        
            messages.success(request, "Producto almacenado correctamente")
        else:
            messages.error(request, "No hay suficiente stock disponible")

    data = {'Productos': producto}
    return render(request, 'core/shop-details.html', data)
  

def main(request):
    return render(request, 'core/main.html')


#carrito
# shoping es donde se almacena cuando aniadimos al carrito 
@login_required
def shopingcart(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    total_precio = 0

    for item in carrito:
        item.total_producto = item.producto.precio * item.cantidad_agregada
        total_precio += item.total_producto

    descuento = Decimal('0.0')
    total_con_descuento = total_precio
    if hasattr(request.user, 'suscripcion'):
            descuento_porcentaje = Decimal('0.1')
            descuento = round(total_precio * descuento_porcentaje)
            total_con_descuento = round(total_precio - descuento)    

    datos = {
        'listarproductos': carrito,
        'total_precio': total_precio,
        'descuento': descuento,
        'total_con_descuento': total_con_descuento,
    }

    return render(request, 'core/shoping-cart.html', datos)


def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            grupo = Group.objects.get(name="Cliente")
            user.groups.add(grupo)
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            #redirigir al home
            return redirect(to="index")
        data["form"] = formulario
    return render(request, 'registration/registro.html',data)



def eliminar_producto(request, id):
    carro = Carrito.objects.get(id=id)
    producto = carro.producto

    # Sumar la cantidad del carrito al stock del producto
    producto.stock += carro.cantidad_agregada
    producto.save()

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
            grupo = Group.objects.get(name="Cliente")
            user.groups.add(grupo)
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            #redirigir al home
            return redirect(to="index")
        data["form"] = formulario    
    return render(request, 'registration/registro.html',data)





@login_required
def suscripcion(request):
    user = request.user
    suscripcion = Suscripcion.objects.filter(usuario=user).first()

    if suscripcion:
        suscrito = True
        fecha_inicio = suscripcion.fecha_inicio.strftime('%m/%d')
        fecha_termino = suscripcion.fecha_finalizacion.strftime('%m/%d')
    else:
        suscrito = False
        fecha_inicio = None
        fecha_termino = None

    if request.method == 'POST':
        form = SuscripcionForm(request.POST)
        if form.is_valid():
            suscripcion = form.save(commit=False)
            suscripcion.usuario = user
            suscripcion.fecha_inicio = timezone.now()
            suscripcion.fecha_finalizacion = suscripcion.fecha_inicio + timedelta(days=30)
            suscripcion.save()

            messages.success(request, '¡Te has suscrito correctamente!')
            return redirect('index')
    else:
        form = SuscripcionForm()

    return render(request, 'core/suscripcion.html', {'form': form, 'suscrito': suscrito, 'fecha_inicio': fecha_inicio, 'fecha_termino': fecha_termino})



@login_required
def cancelar_suscripcion(request):
    suscripcion = Suscripcion.objects.get(usuario=request.user)
    suscripcion.delete()
    messages.success(request, '¡Tu suscripción ha sido cancelada correctamente!')
    return redirect('index')

def seguimiento(request):
    # Obtener todos los pedidos del usuario actual
    pedidos = Pedido.objects.filter(usuario=request.user)

    return render(request, 'core/seguimiento.html', {'pedidos': pedidos})


def cambiar_estado_pedido(request, pedido_id):
    # Obtener el pedido específico
    pedido = Pedido.objects.get(pk=pedido_id)

    if request.method == 'POST':
        # Obtener el nuevo estado seleccionado
        nuevo_estado = request.POST.get('nuevo_estado')

        # Actualizar el estado del pedido
        pedido.estado = nuevo_estado
        pedido.save()
        return redirect('seguimiento')
    return render(request, 'core/seguimiento.html', {'pedido': pedido})



