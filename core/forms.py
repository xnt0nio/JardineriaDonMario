# VAMOS A CREAR UN FORMULARIO QUE SE REUTILIZA EN EL AGREGAR Y ACTUALIZAR
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User





class ProductoForm(ModelForm):

    nombre = forms.CharField(min_length=4,widget=forms.TextInput(attrs={"placeholder":"Ingrese Nombre"}))
    precio = forms.IntegerField(min_value=1,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Precio"}))
    stock = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Stock"}))
    descripcion = forms.CharField(min_length=10,max_length=250,widget=forms.Textarea(attrs={"rows":4}))

    #def clean_nombre(self):
    #    nombre = self.cleaned_data["nombre"]
    #    existe = Producto.objects.filter(nombre__iexact=nombre).exists()

        #if existe:
        #    raise ValidationError("este nombre ya existe")
        #return nombre
    
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
        fields = ['producto', 'cantidad_agregada']

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', "first_name", "last_name", "email", "password1", "password2"]






class SuscripcionForm(forms.ModelForm):
    class Meta:
        model = Suscripcion
        fields = []





