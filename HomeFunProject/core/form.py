from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .validators import TamañoImagenValidator
from .models import FichaResidente , EspacioComun, ReservaEspComun

class CrearCuentaUsuario (forms.ModelForm):
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

class ModReservaEspacioComunForm(forms.ModelForm):
  hora = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
  class Meta:
    model = ReservaEspComun
    fields=['descripcion','hora']

class CrearReservaEspacioComunForm(forms.ModelForm):
  hora = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
  fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
  class Meta:
    model = ReservaEspComun
    fields=['descripcion','fecha','hora','id_espacio_comun','id_residente','estado_reserva']



