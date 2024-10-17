from django.shortcuts import render, redirect
from django.contrib import messages
from .controller import Controller
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from core.form import CrearUsuario, CrearCuentaUsuario
from core.models import FichaResidente, EspacioComun


def home(request):
    return render(request, 'core/home.html')

def inicio(request):
    return render(request, 'core/inicio.html')

def panel_admin(request):
    return render(request, 'core/panel_admin.html')

def admin_espacios_comunes(request):
    espacio_comun = EspacioComun.objects.all()
    datos = {
        'espacio_comun': espacio_comun
    }
    return render(request, 'core/admin_espacios_comunes.html', datos)

def asignar_permisos_colaborador(usuario):
    # Obtener el permiso deseado
    permisos = [
      
    ]
    # Obtener los objetos Permission correspondientes a los nombres de permisos en la lista
    permisos_objetos = Permission.objects.filter(codename__in=permisos)

def asignar_permisos_administrador(usuario):
    # Obtener el permiso deseado
    permisos = [
    
        'view_usuario',
        'add_usuario',
        'change_usuario',
        'delete_usuario',
    ]
    # Obtener los objetos Permission correspondientes a los nombres de permisos en la lista
    permisos_objetos = Permission.objects.filter(codename__in=permisos)

    # Asignar el permiso al usuario
    usuario.user_permissions.add(permisos_objetos)

def registro (request):
    data ={
        'form':CrearUsuario
    }
    if request.method =='POST':
        formulario = CrearUsuario(data= request.POST)
        if formulario.is_valid:
            formulario.save()
            messages.success(request,"Te has registrado correctamente")
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request,user)
            return redirect(to="index_home")
        data["form"] = formulario
    return render(request, 'registration/registro.html',data)



def agregar_administrador(request):
    data = {
        'form': CrearCuentaUsuario
    }
    if request.method == 'POST':
        formulario = CrearCuentaUsuario(data=request.POST)
        if formulario.is_valid():
            print(formulario.cleaned_data["nom_usuario"])
            formulario.save()
            tipo_user = FichaResidente.objects.get(nom_usuario=formulario.cleaned_data["nom_usuario"])
            tipo_user.save()
            messages.success(request, "Te has registrado correctamente")
            usuario = User
            usuario = User.objects.create_user(username=formulario.cleaned_data["nom_usuario"], password=formulario.cleaned_data["password"],first_name=formulario.cleaned_data["nombres"],last_name=formulario.cleaned_data["apellidos"],email=formulario.cleaned_data["correo"],is_staff=0, is_superuser=0)
            asignar_permisos_administrador(usuario)
            user = authenticate(
                username=formulario.cleaned_data["nom_usuario"], password=formulario.cleaned_data["password"])
            login(request, user)
            return redirect(to="home")
        data["form"] = formulario
    return render(request, 'core/agregar_administrador.html', data)