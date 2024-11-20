from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .validators import TamañoImagenValidator
from .models import FichaResidente , EspacioComun, ReservaEspComun, Multa, TipoGastoComun, TipoMulta, GastoComun
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class CrearCuentaUsuario (forms.ModelForm):
   correo = forms.EmailField()
   password = forms.CharField(
        widget=forms.PasswordInput,
        label="Contraseña",
        required=True,
        help_text="Introduce una contraseña segura.",min_length=7,max_length=10
    )
   class Meta:
    model = FichaResidente
    fields=["id_residente","nombre","apellido","correo","direccion","rut","genero","comuna","estado_civil"]

class CrearUsuario(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Contraseña",
        required=True,
        help_text="La contraseña debe tener al menos 8 caracteres y contener un número.",
        min_length=7,
        max_length=10
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirmar Contraseña",
        required=True,
        help_text="Por favor, repite la contraseña.",
        min_length=7,
        max_length=10
    )

    class Meta:
        model = User
        fields = ['username', "first_name", "last_name", "email", "password1", "password2"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Validación para las contraseñas
        if password1 and password2:
            if password1 != password2:
                self.add_error('password2', "Las contraseñas no coinciden.")

        return cleaned_data

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        # Validación usando las reglas de Django
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        # Validación adicional (opcional)
        if len(password) < 7 or len(password) > 10:
            raise ValidationError("La contraseña debe tener entre 7 y 10 caracteres.")
        return password

class ModificarUsuarioForm (forms.ModelForm):
   class Meta:
    model = User
    fields=["first_name","last_name","email"]

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

class CrearMultaForm(forms.ModelForm):
  fecha_ingreso = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
  class Meta:
    model = Multa
    fields=['descripcion','fecha_ingreso','id_dpto','estado_multa','tipo']
    
    
class GenerarMultaForm(forms.ModelForm):
  fecha_ingreso = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
  class Meta:
    model = Multa
    fields=['descripcion','fecha_ingreso','id_dpto','estado_multa']    


class ModificarMultaForm(forms.ModelForm):
  class Meta:
    model = Multa
    fields=['descripcion']


class CrearTipoGastoComunForm(forms.ModelForm):
  class Meta:
    model = TipoGastoComun
    fields =['nombre','monto','reajuste','estado_t_gc']


class ModificarTipoGastoComunForm(forms.ModelForm):
  class Meta:
    model = TipoGastoComun
    fields =['nombre','monto','reajuste','estado_t_gc']


class ModificarFichaResidenteForm (forms.ModelForm):
   correo = forms.EmailField()
   class Meta:
    model = FichaResidente
    fields=["nombre","apellido","correo","direccion","genero","comuna","estado_civil"]


class CrearTipoMultaForm(forms.ModelForm):
  class Meta:
    model = TipoMulta
    fields=['descripcion','monto','estado_t_multa']
    

class ModificarTipoMultaForm(forms.ModelForm):
  class Meta:
    model = TipoMulta
    fields=['descripcion','monto']

class CrearGastoComunForm(forms.ModelForm):
  fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
  class  Meta:
    model= GastoComun
    fields=['nombre','fecha','total','consumo','estado_gc','tipo','id_dpto']


class ModificarGastoComunForm(forms.ModelForm):
  fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
  class  Meta:
    model= GastoComun
    fields=['nombre','fecha','total','consumo','estado_gc','tipo','id_dpto']





