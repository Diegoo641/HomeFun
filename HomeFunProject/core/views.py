from django.shortcuts import render, redirect
from django.contrib import messages
#from .controller import Controller
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from core.form import CrearMultaForm, GenerarMultaForm,CrearUsuario, CrearCuentaUsuario , EspacioComunForm, ModReservaEspacioComunForm, \
    CrearReservaEspacioComunForm, ModificarTipoGastoComunForm,ModificarUsuarioForm, ModificarMultaForm, CrearTipoGastoComunForm
from core.models import FichaResidente, EspacioComun, Estado_EC, ReservaEspComun, Estado_R_EC,GastoComun,Multa,EstadoMulta,\
TipoGastoComun,Estado_T_GC
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .controller import Controller
def es_superusuario_o_staff(user):
    return user.is_superuser or user.is_staff

@login_required


def home(request):
    return render(request, 'core/home.html')

def inicio(request):
    return render(request, 'core/inicio.html')

def panel_admin(request):
    return render(request, 'core/panel_admin.html')

def panel_residente(request):
    return render(request, 'core/panel_residente.html')


def admin_ficha_residentes(request):
    return render(request, 'core/admin_ficha_residentes.html')

def visualizar_morosidad(request):
    return render(request, 'core/visualizar_morosidad.html')


def pagarDeuda(request):
    return render(request, 'core/pagarDeuda.html')


    
def Multas(request):
        return render(request, 'core/Multas.html')


def generar_multa(request):
    datos = {
        'form': GenerarMultaForm()
    }
    if request.method == 'POST':
        formulario = GenerarMultaForm(request.POST , request.FILES)

        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Multa registrada correctamente")
            datos['mensaje'] = "Guardados Correctamente"
            return redirect(to="Multas")
        else:
            print("Error")
    return render(request, 'core/generar_multa.html',datos)   



@user_passes_test(es_superusuario_o_staff)
def admin_espacios_comunes(request):
    espacio_comun = EspacioComun.objects.all()
    datos = {
        'espacio_comun': espacio_comun
    }
    return render(request, 'core/admin_espacios_comunes.html', datos)

def consulta_estado_cuenta(request):
    rut_usuario = request.user.username  # Asumiendo que el nombre de usuario es el RUT
    # Filtrar los gastos comunes según el 'rut'
    residente = FichaResidente.objects.filter(rut=rut_usuario).first()
    print(residente.rut)

    if residente:
        gasto_comun = GastoComun.objects.filter(id_dpto__id_residente__rut=residente.rut)
        print(gasto_comun)
    else:
        gasto_comun = GastoComun.objects.none()
    datos = {
        'gasto_comun': gasto_comun,
        'preference_id':'',
    }
    

    return render(request, 'core/consulta_estado_cuenta.html', datos)

@user_passes_test(es_superusuario_o_staff)
def admin_res_espacios_comunes(request):
    res_espacio_comun = ReservaEspComun.objects.all()
    datos = {
        'res_espacio_comun': res_espacio_comun
    }
    return render(request, 'core/admin_res_espacios_comunes.html', datos)

def crear_espacio_comun(request):
    datos = {
        'form': EspacioComunForm()
    }
    if request.method == 'POST':
        formulario = EspacioComunForm(request.POST , request.FILES)

        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Espacio comun registrado correctamente")
            datos['mensaje'] = "Guardados Correctamente"
            return redirect(to="admin_espacios_comunes")
        else:
            print("Error")
    return render(request, 'core/crear_espacio_comun.html',datos)   

def modificar_espacio_comun(request, id):
    espacioComun = EspacioComun.objects.get(id_espacio_comun=id)
    datos = {
        'form': EspacioComunForm(instance=espacioComun)
    }
    if request.method == 'POST':
        formulario = EspacioComunForm(data=request.POST,files=request.FILES, instance= espacioComun)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto modificado correctamente")
            return redirect(to="admin_espacios_comunes")
        datos = {
            'form': EspacioComunForm(instance=espacioComun),
            'mensaje': "Modificado correctamente"
        }
    return render(request, 'core/modificar_espacio_comun.html', datos)

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


def agregar_administrador (request):
    data ={
        'form':CrearUsuario
    }
    if request.method =='POST':
        formulario = CrearUsuario(data= request.POST)
        if formulario.is_valid:
            formulario.save()
            messages.success(request,"Te has registrado correctamente")
            return redirect(to="home")
        data["form"] = formulario
    return render(request, 'registration/registro.html',data)



def registro(request):
    data = {
        'form': CrearCuentaUsuario
    }
    if request.method == 'POST':
        formulario = CrearCuentaUsuario(data=request.POST)
        if formulario.is_valid():
            print(formulario.cleaned_data["rut"])
            formulario.save()
            messages.success(request, "Has creado la ficha de usuario de manera correcta")
            usuario = User
            usuario = User.objects.create_user(username=formulario.cleaned_data["rut"],first_name=formulario.cleaned_data["nombre"],last_name=formulario.cleaned_data["apellido"],email=formulario.cleaned_data["correo"],is_staff=0, is_superuser=0)
            password = request.POST.get('password')
            usuario.set_password(password)
            usuario.save()
            #asignar_permisos_administrador(usuario)
            # user = authenticate(
            #     username=formulario.cleaned_data["nom_usuario"], password=formulario.cleaned_data["password"])
            # login(request, user)
            return redirect(to="home")
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)

def Validar_Postulacion(request, id):
    postulacionInstr = PostulacionInstr.objects.get(idPostulacion=id)
    datos = {
        'form': PostulacionInstrForm(instance=postulacionInstr)
    }
    if request.method == 'POST':
        formulario = PostulacionInstrForm(
            data=request.POST, instance=postulacionInstr)
        if formulario.is_valid():
            postulacionInstr.estado = "aceptada"
            postulacionInstr.save()
            formulario.save()
            messages.success(request, "Postulación aceptada")
            nombre = postulacionInstr.nombres+" "+postulacionInstr.apellidos
            email = postulacionInstr.correo
            print(email)
            contenido = "¡¡¡Le informamos que su postulación fue aceptada!!!\n\n Para continuar con el proceso, dirigase a nuestras oficinas en:\n  Av. Concha y Toro 1820, 8152857 Puente Alto, Región Metropolitana. \n\n\n ¡Estamos ansiosos de trabajar trabajar con usted! \n\n\n Atte.,\n Dirección de Recursos Humanos. \n Puente Alto."

            # email=EmailMessage("Mensaje de app Django",
            # "Estimad@ {} con la dirección {} escribe lo siguiente:\n\n {}".format(nombre, email, contenido),
            # '',
            email = EmailMessage("Mensaje de app Django",
                                 "Hola! {} :\n\n {}".format(nombre, contenido),
                                 '',
                                 [email],
                                 reply_to=[email])

            email.send()
            return redirect(to="Admin_Postulacion")

        datos = {
            'form': PostulacionInstrForm(instance=postulacionInstr),
            'mensaje': "Correo enviado correctamente"
        }
    return render(request, 'core/Validar_Postulacion.html', datos)

def eliminarEspacioComun(request, id):
    espacioComun = get_object_or_404(EspacioComun, id_espacio_comun=id)
    if request.method == 'POST':
        # Cambiar el estado del espacio común a "eliminado"
        estado_eliminado = get_object_or_404(Estado_EC, id_est_ec=4)  # Get the Estado_EC instance with ID 4
        espacioComun.estado_ec = estado_eliminado
        espacioComun.save()  # Guardar los cambios
        messages.success(request, "Espacio Común Eliminado")
        return redirect(to="admin_espacios_comunes")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/admin_espacios_comunes.html', {
        'form': EspacioComunForm(instance=espacioComun)
    })

def habilitarEspacioComun(request, id):
    espacioComun = get_object_or_404(EspacioComun, id_espacio_comun=id)
    if request.method == 'POST':
        # Cambiar el estado del espacio común a "eliminado"
        estado_eliminado = get_object_or_404(Estado_EC, id_est_ec=1)  # Get the Estado_EC instance with ID 4
        espacioComun.estado_ec = estado_eliminado
        espacioComun.save()  # Guardar los cambios
        messages.success(request, "Espacio Común Habillitado")
        return redirect(to="admin_espacios_comunes")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/admin_espacios_comunes.html', {
        'form': EspacioComunForm(instance=espacioComun)
    })

def cancelarReservaEspacioComun(request, id):
    resEspacioComun = get_object_or_404(ReservaEspComun, id_reserva_esp_comun=id)
    if request.method == 'POST':
        # Cambiar el estado del espacio común a "eliminado"
        estado_eliminado = get_object_or_404(Estado_R_EC, id_est_r_ec=2)  # Get the Estado_EC instance with ID 4
        resEspacioComun.estado_reserva = estado_eliminado
        resEspacioComun.save()  # Guardar los cambios
        messages.success(request, "Espacio Común Eliminado")
        return redirect(to="admin_res_espacios_comunes")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/admin_res_espacios_comunes.html', {
        'form': EspacioComunForm(instance=resEspacioComun)
    })

def modificar_res_espacio_comun(request, id):
    resEspacioComun = ReservaEspComun.objects.get(id_reserva_esp_comun=id)
    datos = {
        'form': ModReservaEspacioComunForm(instance=resEspacioComun)
    }
    if request.method == 'POST':
        formulario = ModReservaEspacioComunForm(data= request.POST, instance= resEspacioComun)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Reserva modificada correctamente")
            return redirect(to="admin_res_espacios_comunes")
        datos = {
            'form': ModReservaEspacioComunForm(instance=resEspacioComun),
            'mensaje': "Modificado correctamente"
        }

    return render(request, 'core/modificar_res_espacio_comun.html', datos)

def crear_res_espacio_comun(request):
    datos = {
        'form': CrearReservaEspacioComunForm()
    }
    if request.method == 'POST':
        formulario = CrearReservaEspacioComunForm(data= request.POST)
        if formulario.is_valid():
            formulario.cleaned_data["estado_reserva"]
            formulario.save()
            messages.success(request,"Espacio comun registrado correctamente")
            datos['mensaje'] = "Guardados Correctamente"
            return redirect(to="admin_res_espacios_comunes")
        else:
            print("Error")
    return render(request, 'core/crear_res_espacio_comun.html',datos)  

@user_passes_test(es_superusuario_o_staff)
def admin_cuentas(request):
    cuentas_user = User.objects.all()
    datos = {
        'cuentas_user': cuentas_user
    }
    return render(request, 'core/admin_cuentas.html', datos)

def desactivarCuenta(request, id):
    user = User.objects.get(id=id)
    print(user)
    if request.method == 'POST':
        # Cambiar el estado del espacio común a "eliminado"
        user.is_active = 0
        user.save()  # Guardar los cambios
        messages.success(request, "Cuenta desactivada")
        return redirect(to="admin_cuentas")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/admin_cuentas.html', {
        'form': CrearUsuario(instance=user)
    })

def activarCuenta(request, id):
    user = User.objects.get(id=id)
    print(user)
    if request.method == 'POST':
        # Cambiar el estado del espacio común a "eliminado"
        user.is_active = 1
        user.save()  # Guardar los cambios
        messages.success(request, "Cuenta activada")
        return redirect(to="admin_cuentas")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/admin_cuentas.html', {
        'form': CrearUsuario(instance=user)
    })

def crear_cuenta(request):
    datos = {
        'form': CrearUsuario()
    }
    if request.method == 'POST':
        formulario = CrearUsuario(data= request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Cuenta creada correctamente")
            datos['mensaje'] = "Guardados Correctamente"
            return redirect(to="admin_cuentas")
        else:
            print("Error")
    return render(request, 'core/crear_cuenta.html',datos) 

def modificar_cuenta(request, id):
    cuenta_user = User.objects.get(id=id)
    datos = {
        'form': ModificarUsuarioForm(instance=cuenta_user)
    }
    if request.method == 'POST':
        formulario = ModificarUsuarioForm(data= request.POST, instance= cuenta_user)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Cuenta modificada correctamente")
            return redirect(to="admin_cuentas")
        datos = {
            'form': ModificarUsuarioForm(instance=cuenta_user),
            'mensaje': "Modificado correctamente"
        }

    return render(request, 'core/modificar_cuenta.html', datos)

@user_passes_test(es_superusuario_o_staff)
def admin_multas(request):
    multa = Multa.objects.all()
    datos = {
        'multa': multa
    }
    return render(request, 'core/admin_multas.html', datos)


def crear_multa(request):
    datos = {
        'form': CrearMultaForm()
    }
    if request.method == 'POST':
        formulario = CrearMultaForm(data= request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Cuenta creada correctamente")
            datos['mensaje'] = "Guardados Correctamente"
            return redirect(to="admin_multas")
        else:
            print("Error")
    return render(request, 'core/crear_multa.html',datos) 


def modificar_multa(request, id):
    multa = Multa.objects.get(id_multa=id)
    datos = {
        'form': ModificarMultaForm(instance=multa)
    }
    if request.method == 'POST':
        formulario = ModificarMultaForm(data= request.POST, instance= multa)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Multa modificada correctamente")
            return redirect(to="admin_multas")
        datos = {
            'form': ModificarMultaForm(instance=multa),
            'mensaje': "Modificado correctamente"
        }

    return render(request, 'core/modificar_multa.html', datos)

def cancelarMulta(request, id):
    multa = Multa.objects.get(id_multa=id)
    if request.method == 'POST':
        # Cambiar el estado del espacio común a "eliminado"
        estado_cancelado = get_object_or_404(EstadoMulta, id_est_multa=3)  # Get the Estado_EC instance with ID 4

        multa.estado_multa = estado_cancelado
        multa.save()  # Guardar los cambios
        messages.success(request, "Multa Cancelada")
        return redirect(to="admin_multas")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/admin_multas.html', {
        'form': CrearMultaForm(instance=multa)
    })

def pagarMulta(request, id):
    multa = Multa.objects.get(id_multa=id)
    print(multa)
    if request.method == 'POST':
        # Cambiar el estado del espacio común a "eliminado"
        estado_pagado = get_object_or_404(EstadoMulta, id_est_multa=2)  # Get the Estado_EC instance with ID 4
        multa.estado_multa = estado_pagado
        multa.save()  # Guardar los cambios
        messages.success(request, "Multa pagada")
        return redirect(to="admin_multas")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/admin_multas.html', {
        'form': CrearMultaForm(instance=multa)
    })

def eliminarMulta(request, id):
    multa = Multa.objects.get(id_multa=id)
    print(multa)
    if request.method == 'POST':
        # Cambiar el estado del espacio común a "eliminado"
        estado_pagado = get_object_or_404(EstadoMulta, id_est_multa=4)  # Get the Estado_EC instance with ID 4
        multa.estado_multa = estado_pagado
        multa.save()  # Guardar los cambios
        messages.success(request, "Multa Eliminada")
        return redirect(to="admin_multas")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/admin_multas.html', {
        'form': CrearMultaForm(instance=multa)
    })

@user_passes_test(es_superusuario_o_staff)
def admin_tipo_gasto_comun(request):
    gasto_comun = TipoGastoComun.objects.all()
    datos = {
        'gasto_comun': gasto_comun
    }
    return render(request, 'core/admin_tipo_gasto_comun.html', datos)

def crear_tipo_gasto_comun(request):
    datos = {
        'form': CrearTipoGastoComunForm()
    }
    if request.method == 'POST':
        formulario = CrearTipoGastoComunForm(data= request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Tipo de gasto comun creado correctamente")
            datos['mensaje'] = "Guardados Correctamente"
            return redirect(to="admin_tipo_gasto_comun")
        else:
            print("Error")
    return render(request, 'core/crear_tipo_gasto_comun.html',datos) 


def desactivarTipoGastoComun(request, id):
    gasto_comun = get_object_or_404(TipoGastoComun, id_t_gc=id)
    if request.method == 'POST':
        # Cambiar el estado del espacio común a "eliminado"
        estado_eliminado = get_object_or_404(Estado_T_GC, id_est_t_gc=2)  # Get the Estado_EC instance with ID 4
        gasto_comun.estado_t_gc = estado_eliminado
        gasto_comun.save()  # Guardar los cambios
        messages.success(request, "Tipo de gasto comu desactivado")
        return redirect(to="admin_tipo_gasto_comun")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/admin_tipo_gasto_comun.html', {
        'form': EspacioComunForm(instance=gasto_comun)
    })

def activarTipoGastoComun(request, id):
    gasto_comun = get_object_or_404(TipoGastoComun, id_t_gc=id)
    if request.method == 'POST':
        # Cambiar el estado del espacio común a "eliminado"
        estado_activado = get_object_or_404(Estado_T_GC, id_est_t_gc=1)  # Get the Estado_EC instance with ID 4
        gasto_comun.estado_t_gc = estado_activado
        gasto_comun.save()  # Guardar los cambios
        messages.success(request, "Tipo de gasto comu activado")
        return redirect(to="admin_tipo_gasto_comun")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/admin_tipo_gasto_comun.html', {
        'form': EspacioComunForm(instance=gasto_comun)
    })
    
def modificar_tipo_gasto_comun(request, id):
    tipo_gasto = TipoGastoComun.objects.get(id_t_gc=id)
    datos = {
        'form': ModificarTipoGastoComunForm(instance=tipo_gasto)
    }
    if request.method == 'POST':
        formulario = ModificarTipoGastoComunForm(data= request.POST, instance= tipo_gasto)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Multa modificada correctamente")
            return redirect(to="admin_tipo_gasto_comun")
        datos = {
            'form': ModificarTipoGastoComunForm(instance=tipo_gasto),
            'mensaje': "Modificado correctamente"
        }
    return render(request, 'core/modificar_tipo_gasto_comun.html', datos)