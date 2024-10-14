from django import forms
from .models import pedido


#Quiero que validez los datos de este formulario y que se guarde en la base de datos
class PedidoForm(forms.ModelForm):
    class Meta:
        model = pedido
        fields = ['nombre', 'apellido', 'telefono', 'email', 'direccion_linea_1', 'direccion_linea_2', 'ciudad', 'estado', 'pais', 'nota_pedido']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'direccion_linea_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Direccion Linea 1'}),
            'direccion_linea_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Direccion Linea 2'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pais'}),
            'nota_pedido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nota Pedido'}),
        }
