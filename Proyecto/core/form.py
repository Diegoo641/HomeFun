from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .validators import TamañoImagenValidator


class CrearCuentaUsuario (forms.ModelForm):
   nombres = forms.CharField(min_length=3, max_length=100)
   apellidos = forms.CharField(min_length=3, max_length=100)
   password = forms.CharField(min_length=3, max_length=10, required=True)
   fecha_nac = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
   correo = forms.EmailField()

   class Meta:
    model = Usuario
    fields=["nombres","apellidos","nom_usuario","correo","direccion","fecha_nac"]

class CrearUsuario (UserCreationForm):
   class Meta:
    model = User
    fields=['username',"first_name","last_name","email","password1","password2"]




