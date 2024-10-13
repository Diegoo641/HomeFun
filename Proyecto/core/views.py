from django.shortcuts import render, redirect
from django.contrib import messages
from .controller import Controller
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission


carrito={
    'nombre':'',
    'total':0
}
total=0
productosCarrito=[]

cantAnwo=0
CantBod=0
cantidad =[]
cant_pro = {}
# Create your views here.

def home(request):
    return render(request, 'core/home.html')
def inicio(request):
    return render(request, 'core/inicio.html')


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

def registro(request):
    data = {
        'form': CrearCuentaUsuario
    }
    if request.method == 'POST':
        formulario = CrearCuentaUsuario(data=request.POST)
        if formulario.is_valid():
            print(formulario.cleaned_data["nom_usuario"])
            formulario.save()
            tipo_user = Usuario.objects.get(nom_usuario=formulario.cleaned_data["nom_usuario"])
            tipo_user.tipo_usr = Tipo_usuario.objects.get(id=3)
            tipo_user.save()
            messages.success(request, "Te has registrado correctamente")
            usuario = User
            usuario = User.objects.create_user(username=formulario.cleaned_data["nom_usuario"], password=formulario.cleaned_data["password"],first_name=formulario.cleaned_data["nombres"],last_name=formulario.cleaned_data["apellidos"],email=formulario.cleaned_data["correo"])
            user = authenticate(
                username=formulario.cleaned_data["nom_usuario"], password=formulario.cleaned_data["password"])
            login(request, user)
            return redirect(to="inicio")
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)

def agregar_colaborador(request):
    data = {
        'form': CrearCuentaUsuario
    }
    if request.method == 'POST':
        formulario = CrearCuentaUsuario(data=request.POST)
        if formulario.is_valid():
            print(formulario.cleaned_data["nom_usuario"])
            formulario.save()
            tipo_user = Usuario.objects.get(nom_usuario=formulario.cleaned_data["nom_usuario"])
            tipo_user.tipo_usr = Tipo_usuario.objects.get(id=2)
            tipo_user.save()
            messages.success(request, "Te has registrado correctamente")
            usuario = User
            usuario = User.objects.create_user(username=formulario.cleaned_data["nom_usuario"], password=formulario.cleaned_data["password"],first_name=formulario.cleaned_data["nombres"],last_name=formulario.cleaned_data["apellidos"],email=formulario.cleaned_data["correo"],is_staff=1,is_superuser=0)
            asignar_permisos_colaborador(usuario)
            user = authenticate(
                username=formulario.cleaned_data["nom_usuario"], password=formulario.cleaned_data["password"])
            login(request, user)
            return redirect(to="inicio")
        data["form"] = formulario
    return render(request, 'core/agregar_colaborador.html', data)

def agregar_administrador(request):
    data = {
        'form': CrearCuentaUsuario
    }
    if request.method == 'POST':
        formulario = CrearCuentaUsuario(data=request.POST)
        if formulario.is_valid():
            print(formulario.cleaned_data["nom_usuario"])
            formulario.save()
            tipo_user = Usuario.objects.get(nom_usuario=formulario.cleaned_data["nom_usuario"])
            tipo_user.tipo_usr = Tipo_usuario.objects.get(id=1)
            tipo_user.save()
            messages.success(request, "Te has registrado correctamente")
            usuario = User
            usuario = User.objects.create_user(username=formulario.cleaned_data["nom_usuario"], password=formulario.cleaned_data["password"],first_name=formulario.cleaned_data["nombres"],last_name=formulario.cleaned_data["apellidos"],email=formulario.cleaned_data["correo"],is_staff=0, is_superuser=1)
            asignar_permisos_administrador(usuario)
            user = authenticate(
                username=formulario.cleaned_data["nom_usuario"], password=formulario.cleaned_data["password"])
            login(request, user)
            return redirect(to="inicio")
        data["form"] = formulario
    return render(request, 'core/agregar_administrador.html', data)