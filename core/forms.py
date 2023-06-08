# VAMOS A CREAR UN FORMULARIO QUE SE REUTILIZA EN EL AGREGAR Y ACTUALIZAR
from datetime import date
from django import forms
from django.forms import ModelForm
from .models import *
from django.views.generic.edit import UpdateView


class ProductoForm(ModelForm):

    nombre = forms.CharField(min_length=4,widget=forms.TextInput(attrs={"placeholder":"Ingrese Nombre"}))
    precio = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Precio"}))
    stock = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Stock"}))
    descripcion = forms.CharField(min_length=10,max_length=250,widget=forms.Textarea(attrs={"rows":4}))
    
    
    class Meta:
        model = Producto
        #fields = ['nombre','precio','stock','descripcion','tipo']
        fields = '__all__'



        widgets = {
            'vencimiento' : forms.DateInput(attrs={'type': 'date'})
        }


class CarritoForm(forms.ModelForm):
    class Meta:
        model = Carrito
        fields = ['nombre_producto', 'precio_producto', 'imagen', 'cantidad_agregada']