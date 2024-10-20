from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .validators import TamañoImagenValidator
from .models import FichaResidente , EspacioComun, ReservaEspComun

class CrearCuentaUsuario (forms.ModelForm):
   nombres = forms.CharField(min_length=3, max_length=100)
   apellidos = forms.CharField(min_length=3, max_length=100)
   fecha_nac = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
   correo = forms.EmailField()

   class Meta:
    model = FichaResidente
    fields=["id_residente","nombre","apellido","correo","direccion","rut","genero","comuna","estado_civil"]

class CrearUsuario (UserCreationForm):
   class Meta:
    model = User
    fields=['username',"first_name","last_name","email","password1","password2"]


class EspacioComunForm(forms.ModelForm):
  class Meta:
    model = EspacioComun
    fields=['nombre','descripcion','ubicacion','imagen','valor','id_comunidad','estado_ec']

class ReservaEspacioComunForm(forms.ModelForm):
  hora = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
  class Meta:
    model = ReservaEspComun
    fields=['descripcion','fecha','hora','id_espacio_comun','id_residente']



