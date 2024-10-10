from django import forms
from .models import Cuenta
from .choices import generos
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese Contraseña','class':'form-control'}))
    verificar_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repita Contraseña','class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Ingrese su Email','class':'form-control'}))
    telefono = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su Telefono','class':'form-control'}))
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'día/mes/año','class':'form-control','type':'date'}))
    genero = forms.ChoiceField(choices=generos,widget=forms.Select(attrs={'class':'form-control','type':'select'}))
    nombre = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su Nombre','class':'form-control'}))
    apellido = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su Apellido','class':'form-control'}))

    class Meta:
        model = Cuenta
        fields = ['nombre', 'apellido', 'telefono', 'fecha_nacimiento', 'email', 'password', 'verificar_password', 'genero']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Ingrese Contraseña','class':'form-control'}),
            'verificar_password': forms.PasswordInput(attrs={'placeholder': 'Repita Contraseña','class':'form-control'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise ValidationError(_('La contraseña debe tener al menos 6 caracteres.'))
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('La contraseña debe contener al menos un número.'))
        if not any(char.isupper() for char in password):
            raise ValidationError(_('La contraseña debe contener al menos una letra mayúscula.'))
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for char in password):
            raise ValidationError(_('La contraseña debe contener al menos un símbolo.'))
        return password

    def clean_verificar_password(self):
        password = self.cleaned_data.get('password')
        verificar_password = self.cleaned_data.get('verificar_password')
        if password and verificar_password and password != verificar_password:
            raise ValidationError(_('Las contraseñas no coinciden.'))
        return verificar_password

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        today = datetime.date.today()
        age = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        if age < 18:
            raise ValidationError(_('Debe tener al menos 18 años para registrarse.'))
        if age > 65:
            raise ValidationError(_('Debe tener menos de 65 años para registrarse.'))
        return fecha_nacimiento
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.startswith('+569'):
            raise ValidationError(_('El número de teléfono debe comenzar con +569.'))
        if not telefono[1:].isdigit():
            raise ValidationError(_('El número de teléfono debe contener solo dígitos después del "+".'))
        if len(telefono) != 12:
            raise ValidationError(_('El número de teléfono debe tener 12 dígitos incluyendo el "+569".'))
        return telefono
    
