from django.shortcuts import render, redirect
from django.contrib import messages
#from .controller import Controller
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from core.form import CrearGastoComunForm, CrearMultaForm, CrearReservaEspacioComunResForm, CrearTipoMultaForm, GenerarMultaForm,CrearUsuario, CrearCuentaUsuario , EspacioComunForm, ModReservaEspacioComunForm, \
    CrearReservaEspacioComunForm, ModificarDepartamentoForm, ModificarFichaResidenteForm, ModificarGastoComunForm, ModificarTipoGastoComunForm, ModificarTipoMultaForm,ModificarUsuarioForm, ModificarMultaForm, CrearTipoGastoComunForm
from core.models import Estado_GC, Estado_T_GC, EstadoTipoMulta, FichaResidente, EspacioComun, Estado_EC, ReservaEspComun, Estado_R_EC,GastoComun,Multa,EstadoMulta,\
TipoGastoComun, Estado_residente, TipoMulta
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .controller import Controller
import mercadopago
from django.core.mail import EmailMessage
from django.db.models import Sum, Count




total = 0
total_g = 0
pagar=[]


def es_superusuario_o_staff(user):
    return user.is_superuser or user.is_staff

@login_required
def home(request):
    return render(request, 'core/home.html')

def inicio(request):
    return render(request, 'core/inicio.html')


@login_required
def seleccion_tipo_usuario(request):
    return render(request, 'core/seleccion_tipo_usuario.html')

def seleccion_pago(request):
    return render(request, 'core/seleccion_pago.html')


def panel_admin(request):
    residentes = FichaResidente.objects.filter(estado_id=1)
    cant_activos = residentes.count()
    morosos = GastoComun.objects.filter(estado_gc=3).values('id_dpto__id_residente__rut').annotate(total_monto=Sum('total'))
    cant_morosos = morosos.count()
    reservas = (ReservaEspComun.objects
            .filter(estado_reserva=1)
            .values('id_espacio_comun__nombre')
            .annotate(total_reservas=Count('id_reserva_esp_comun'))
            .order_by('-total_reservas')[:5])
    print(reservas)
    labels = [reserva['id_espacio_comun__nombre'] for reserva in reservas]
    data = [reserva['total_reservas'] for reserva in reservas]
    
  
    data={
       'residentes':residentes,
       'morosos': morosos,
       'cant_morosos': cant_morosos,
       'cant_activos': cant_activos,
       'reservas': reservas,
       'labels': json.dumps(labels),
       'data': json.dumps(data),
    }
    print(labels)
    return render(request, 'core/panel_admin.html',data)

def panel_residente(request):
    return render(request, 'core/panel_residente.html')


def visualizar_morosidad(request):
    gasto_comun = GastoComun.objects.filter(estado_gc=3)
    data = {
        'gasto_comun':gasto_comun
    }
    return render(request, 'core/visualizar_morosidad.html',data)


def pagarDeuda(request):
    return render(request, 'core/pagarDeuda.html')


    
def Multas(request):
    multa = Multa.objects.all()
    datos = {
        'multa': multa
    }
    return render(request, 'core/Multas.html',datos)


def generar_multa(request):
    datos = {
        'form': CrearMultaForm()
    }
    if request.method == 'POST':
        formulario = CrearMultaForm(request.POST , request.FILES)

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
            messages.success(request,"Espacio común registrado correctamente")
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
            messages.success(request, "Espacio común modificado correctamente")
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
            messages.success(request,"Registro creado correctamente")
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
            contenido = "¡¡¡Le informamos que su reserva se ha creado su cuenta de manera correcya!!!\n\n Datos de cueta:\n Nombre usuario : {} \n Pass : {}\n  Para ingresar al sistema ingrese a la siguiente URL\n http://127.0.0.1:8000/accounts/login/ \nDesde ya muchas gracias.\nSaludos".format(usuario.username,password)
            email = EmailMessage("Reservas HomeFun",
                                 "Hola! {} :\n\n {}".format(usuario.first_name, contenido),
                                 '',
                                 [usuario.email],
                                 reply_to=[usuario.email])
            email.send()
            return redirect(to="home")
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)

def Validar_Postulacion(request, id):
    return render(request, 'core/Validar_Postulacion.html')

def eliminarEspacioComun(request, id):
    espacioComun = get_object_or_404(EspacioComun, id_espacio_comun=id)
    if request.method == 'POST':
        # Cambiar el estado del espacio común a "eliminado"
        estado_eliminado = get_object_or_404(Estado_EC, id_est_ec=4)  # Get the Estado_EC instance with ID 4
        espacioComun.estado_ec = estado_eliminado
        espacioComun.save()  # Guardar los cambios
        messages.success(request, "Espacio común eliminado correctamente")
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
        messages.success(request, "Espacio común habillitado")
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
        messages.success(request,"Reserva de espacio común cancelada correctamente")
        residente = resEspacioComun.id_residente  # Esto te da acceso al objeto FichaResidente
        rut_residente = residente.rut
        descripcion = resEspacioComun.descripcion
        fecha = resEspacioComun.fecha
        hora = resEspacioComun.hora
        espacio_comun = resEspacioComun.id_espacio_comun
        # Filtrar los gastos comunes según el 'rut'
        residente = FichaResidente.objects.filter(rut=rut_residente).first()
        print(residente)
        contenido = "Le informamos que su reserva se ha cancelado.\n\n Los datos de reserva son:\n Descripcion : {} \n Fecha : {}\n Hora: {}\n Espacio común: {} \n Para revisar el detalle ingresar a la siguiente URL\n http://127.0.0.1:8000/res_espacios_comunes \nQue tengas un excelente día.\nSaluda afectuosamente la administración".format(descripcion,fecha,hora,espacio_comun)
        email = EmailMessage("Reservas HomeFun",
                             "Hola! {} :\n\n {}".format(residente.nombre, contenido),
                             '',
                             [residente.correo],
                             reply_to=[residente.correo])
        email.send()
        messages.success(request, "Reserva cancelada")
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
            reserva = formulario.save()
            messages.success(request,"Reserva modificada correctamente")
            residente = reserva.id_residente  # Esto te da acceso al objeto FichaResidente
            rut_residente = residente.rut
            descripcion = resEspacioComun.descripcion
            hora = resEspacioComun.hora
            espacio_comun = resEspacioComun.id_espacio_comun
            fecha= resEspacioComun.fecha
            datos['mensaje'] = "Guardados Correctamente"
            # Filtrar los gastos comunes según el 'rut'
            residente = FichaResidente.objects.filter(rut=rut_residente).first()
            print(residente)
            contenido = "Le informamos que su reserva se ha modificado de manera correcta\n\n Datos de reserva:\n Descripción : {} \n Fecha : {}\n Hora: {}\n Espacio común: {} \n Para revisar el detalle ingresar a la siguiente URL\n http://127.0.0.1:8000/res_espacios_comunes \nDesde ya muchas gracias.\nSaludos".format(descripcion,fecha,hora,espacio_comun)
            email = EmailMessage("Reservas HomeFun",
                                 "Hola! {} :\n\n {}".format(residente.nombre, contenido),
                                 '',
                                 [residente.correo],
                                 reply_to=[residente.correo])
            email.send()
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
            reserva = formulario.save()
            messages.success(request,"Espacio común reservado correctamente")
            print(formulario)
            rut_residente = formulario.cleaned_data["id_residente"].rut
            print(rut_residente)
            descripcion = formulario.cleaned_data["descripcion"]
            fecha = formulario.cleaned_data["fecha"]
            hora = formulario.cleaned_data["hora"]
            espacio_comun = formulario.cleaned_data["id_espacio_comun"]
            datos['mensaje'] = "Guardados correctamente"
            # Filtrar los gastos comunes según el 'rut'
            residente = FichaResidente.objects.filter(rut=rut_residente).first()
            print(residente)
            contenido = "Le informamos que su reserva se ha realizado de manera correcta\n\n Datos de reserva:\n Descripción : {} \n Fecha : {}\n Hora: {}\n Espacio común: {} \n Para revisar el detalle ingresar a la siguiente URL\n http://127.0.0.1:8000/res_espacios_comunes \nDesde ya muchas gracias.\nSaludos".format(descripcion,fecha,hora,espacio_comun)
            email = EmailMessage("Reservas HomeFun",
                                 "¡Hola! {} :\n\n {}".format(residente.nombre, contenido),
                                 '',
                                 [residente.correo],
                                 reply_to=[residente.correo])
            email.send()
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
        'form': CrearUsuario()  # Crear una instancia vacía del formulario
    }

    if request.method == 'POST':
        formulario = CrearUsuario(request.POST)  # Pasar los datos del formulario al POST
        if formulario.is_valid():
            # Guardar el usuario si el formulario es válido
            formulario.save()
            username = formulario.cleaned_data['username']
            password = formulario.cleaned_data['password1']
            usuario = User.objects.get(username=username)
            usuario.is_superuser = 1
            usuario.save()
            messages.success(request, "Cuenta creada correctamente")
            datos['mensaje'] = "Guardados Correctamente"
            contenido = "Le informamos que su cuenta se ha craedo correctamente\n\n Datos de cueta:\n Nombre usuario : {} \n Contraseña : {}\n  Para ingresar al sistema ingrese a la siguiente URL\n http://127.0.0.1:8000/accounts/login/ \nDesde ya muchas gracias.\nSaludos".format(usuario.username,password)
            email = EmailMessage("Reservas HomeFun",
                                 "Hola! {} :\n\n {}".format(usuario.first_name, contenido),
                                 '',
                                 [usuario.email],
                                 reply_to=[usuario.email])
            email.send()
            return redirect(to="admin_cuentas")
        else:
            # Si el formulario no es válido, pasamos el formulario con los errores
            datos['form'] = formulario  # Aquí se pasan los errores al formulario
            # No es necesario hacer nada más porque Django Crispy Forms maneja la visualización de errores

    return render(request, 'core/crear_cuenta.html', datos)
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
            messages.success(request,"Multa creada correctamente")
            datos['mensaje'] = "Guardados Correctamente"
            return redirect(to="Multas")
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
            messages.success(request, "Datos modificados correctamente")
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
        return redirect(to="Multas")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/Multas.html', {
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
        return redirect(to="Multas")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/Multas.html', {
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
        return redirect(to="Multas")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/Multas.html', {
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
            messages.success(request,"Tipo de gasto común creado correctamente")
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
        messages.success(request, "Tipo de gasto común desactivado")
        return redirect(to="admin_tipo_gasto_comun")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/admin_tipo_gasto_comun.html', {
        'form': EspacioComunForm(instance=gasto_comun)
    })

def activarTipoGastoComun(request, id):
    gasto_comun = get_object_or_404(TipoGastoComun, id_t_gc=id)
    if request.method == 'POST':
        estado_activado = get_object_or_404(Estado_T_GC, id_est_t_gc=1)  
        gasto_comun.estado_t_gc = estado_activado
        gasto_comun.save() 
        messages.success(request, "Tipo de gasto común activado")
        return redirect(to="admin_tipo_gasto_comun")
    return render(request, 'core/admin_tipo_gasto_comun.html', {
        'form': EspacioComunForm(instance=gasto_comun)})
    
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

@user_passes_test(es_superusuario_o_staff)
def admin_ficha_residentes(request):
    residentes = FichaResidente.objects.all()
    datos = {
        'residentes': residentes
    }
    return render(request, 'core/admin_ficha_residentes.html',datos)

def modificar_ficha_residente(request, id):
    residente = FichaResidente.objects.get(id_residente=id)
    datos = {
        'form': ModificarFichaResidenteForm(instance=residente)
    }
    if request.method == 'POST':
        formulario = ModificarFichaResidenteForm(data= request.POST, instance= residente)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Ficha de residente modificada correctamente")
            return redirect(to="admin_ficha_residentes")
        datos = {
            'form': ModificarFichaResidenteForm(instance=residente),
            'mensaje': "Modificado correctamente"
        }
    return render(request, 'core/modificar_ficha_residente.html', datos)

def desactivarFichaResidente(request, id):
    residente = get_object_or_404(FichaResidente, id_residente=id)
    if request.method == 'POST':
        estado_eliminado = get_object_or_404(Estado_residente, id_est_r=2)
        residente.estado = estado_eliminado
        residente.save()  # Guardar los cambios
        messages.success(request, "Ficha de residente desactivada correctamente")
        return redirect(to="admin_ficha_residentes")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/admin_ficha_residentes.html', {
        'form': EspacioComunForm(instance=residente)})

def activarFichaResidente(request, id):
    residente = get_object_or_404(FichaResidente, id_residente=id)
    if request.method == 'POST':
        estado_activado = get_object_or_404(Estado_residente, id_est_r=1)  
        residente.estado = estado_activado
        residente.save()  # Guardar los cambios
        messages.success(request, "Ficha de residente activada correctamente")
        return redirect(to="admin_ficha_residentes")

    return render(request, 'core/admin_tipo_gasto_comun.html', {
        'form': EspacioComunForm(instance=residente)
    })
    

@user_passes_test(es_superusuario_o_staff)
def admin_tipo_multas(request):
    tipo_multa = TipoMulta.objects.all()
    datos = {
        'tipo_multa': tipo_multa
    }
    return render(request, 'core/admin_tipo_multas.html', datos)


def crear_tipo_multa(request):
    datos = {
        'form': CrearTipoMultaForm()
    }
    if request.method == 'POST':
        formulario = CrearTipoMultaForm(data= request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Tipo de multa creada correctamente")
            datos['mensaje'] = "Guardados Correctamente"
            return redirect(to="admin_tipo_multas")
        else:
            print("Error")
    return render(request, 'core/crear_tipo_multa.html',datos) 


def modificar_tipo_multa(request, id):
    tipo_multa = TipoMulta.objects.get(id_t_multa=id)
    datos = {
        'form': ModificarTipoMultaForm(instance=tipo_multa)
    }
    if request.method == 'POST':
        formulario = ModificarTipoMultaForm(data= request.POST, instance= tipo_multa)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Multa modificada correctamente")
            return redirect(to="admin_tipo_multas")
        datos = {
            'form': ModificarTipoMultaForm(instance=tipo_multa),
            'mensaje': "Modificado correctamente"
        }

    return render(request, 'core/modificar_tipo_multa.html', datos)



def desactivarTipoMulta(request, id):
    tipo_multa = get_object_or_404(TipoMulta, id_t_multa=id)
    if request.method == 'POST':
        # Cambiar el estado del espacio común a "eliminado"
        estado_desactivado = get_object_or_404(EstadoTipoMulta, id_est_t_multa=2)  # Get the Estado_EC instance with ID 4
        tipo_multa.estado_t_multa = estado_desactivado
        tipo_multa.save()  # Guardar los cambios
        messages.success(request, "Tipo de multa desactivado")
        return redirect(to="admin_tipo_multas")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/admin_tipo_multas.html', {
        'form': CrearTipoMultaForm(instance=tipo_multa)})

def activarTipoMulta(request, id):
    tipo_multa = get_object_or_404(TipoMulta, id_t_multa=id)
    if request.method == 'POST':
        estado_activado = get_object_or_404(EstadoTipoMulta, id_est_t_multa=1)
        tipo_multa.estado_t_multa = estado_activado
        tipo_multa.save() 
        messages.success(request, "Tipo de multa activado")
        return redirect(to="admin_tipo_gasto_comun")
    return render(request, 'core/admin_tipo_gasto_comun.html', {
        'form': CrearTipoMultaForm(instance=tipo_multa)})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def agregarPago(request, id):
    if request.method == 'POST':
        try:
            gasto = GastoComun.objects.get(id_gc=id)
            seleccionados_gc = request.session.get('seleccionados_gc', [])
            
            if id not in seleccionados_gc:
                seleccionados_gc.append(id)
                request.session['seleccionados_gc'] = seleccionados_gc
                
                total_actual = request.session.get('total_g', 0)
                request.session['total_g'] = total_actual + gasto.total

                # Regenerar la preferencia con el nuevo total
                controler = Controller()
                preference = controler.pagar(request.session['total_g'])

                return JsonResponse({
                    'total_g': request.session['total_g'],
                    'preference_id': preference["response"]["id"]
                }, status=200)
            return JsonResponse({'error': 'Gasto existente'}, status=400)
        except GastoComun.DoesNotExist:
            return JsonResponse({'error': 'Gasto no encontrado'}, status=404)
    return JsonResponse({'error': 'Método no permitido'}, status=405)



@csrf_exempt
def removerPago(request, id):
    if request.method == 'POST':
        try:
            gasto = GastoComun.objects.get(id_gc=id)
            # Obtener la lista actual de seleccionados desde la sesión
            seleccionados_gc = request.session.get('seleccionados_gc', [])
            
            # Eliminar el gasto de la lista
            if id in seleccionados_gc:
                seleccionados_gc.remove(id)
                request.session['seleccionados_gc'] = seleccionados_gc
            
            total_actual = request.session.get('total_g', 0)
            request.session['total_g'] = max(0, total_actual - gasto.total)  # Evitar negativos
            return JsonResponse({'total_g': request.session['total_g']}, status=200)
        except GastoComun.DoesNotExist:
            return JsonResponse({'error': 'Gasto no encontrado'}, status=404)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def admin_gastos_comunes(request):

    gasto_comun = GastoComun.objects.all()

    datos = {
        'gasto_comun': gasto_comun,
    }

    return render(request, 'core/admin_gastos_comunes.html', datos)


def crear_gasto_comun(request):
    datos = {
        'form': CrearGastoComunForm()
    }
    if request.method == 'POST':
        formulario = CrearGastoComunForm(data= request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Tipo de gasto común creado correctamente")
            datos['mensaje'] = "Guardados Correctamente"
            return redirect(to="admin_gastos_comunes")
        else:
            print("Error")
    return render(request, 'core/crear_gasto_comun.html',datos) 


def desactivarGastoComun(request, id):
    gasto_comun = get_object_or_404(GastoComun, id_gc=id)
    if request.method == 'POST':
        # Cambiar el estado del espacio común a "eliminado"
        estado_eliminado = get_object_or_404(Estado_GC, id_est_gc=4)  # Get the Estado_EC instance with ID 4
        gasto_comun.estado_gc = estado_eliminado
        gasto_comun.save()  # Guardar los cambios
        messages.success(request, "Tipo de gasto común desactivado")
        return redirect(to="admin_gastos_comunes")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/admin_gastos_comunes.html', {
        'form': CrearGastoComunForm(instance=gasto_comun)
    })

def activarGastoComun(request, id):
    gasto_comun = get_object_or_404(GastoComun, id_gc=id)
    if request.method == 'POST':
        estado_activado = get_object_or_404(Estado_GC, id_est_gc=2)  
        gasto_comun.estado_gc = estado_activado
        gasto_comun.save() 
        messages.success(request, "Tipo de gasto común activado")
        return redirect(to="admin_gastos_comunes")
    return render(request, 'core/admin_gastos_comunes.html', {
        'form': CrearGastoComunForm(instance=gasto_comun)})

def pagarGastoComun(request, id):
    gasto_comun = get_object_or_404(GastoComun, id_gc=id)
    if request.method == 'POST':
        estado_activado = get_object_or_404(Estado_GC, id_est_gc=1)  
        gasto_comun.estado_gc = estado_activado
        gasto_comun.save() 
        messages.success(request, "Gasto común pagado")
        return redirect(to="admin_gastos_comunes")
    return render(request, 'core/admin_gastos_comunes.html', {
        'form': CrearGastoComunForm(instance=gasto_comun)})

def modificar_gasto_comun(request, id):
    gasto_comun = GastoComun.objects.get(id_gc=id)
    datos = {
        'form': ModificarGastoComunForm(instance=gasto_comun)
    }
    if request.method == 'POST':
        formulario = ModificarGastoComunForm(data= request.POST, instance= gasto_comun)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Gasto común modificada correctamente")
            return redirect(to="admin_tipo_gasto_comun")
        datos = {
            'form': ModificarGastoComunForm(instance=gasto_comun),
            'mensaje': "Modificado correctamente"
        }
    return render(request, 'core/modificar_tipo_gasto_comun.html', datos)

    
def modificar_gasto_comun(request, id):
    gasto_comun = GastoComun.objects.get(id_gc=id)
    datos = {
        'form': ModificarGastoComunForm(instance=gasto_comun)
    }
    if request.method == 'POST':
        formulario = ModificarGastoComunForm(data= request.POST, instance= gasto_comun)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Gasto común modificado correctamente")
            return redirect(to="admin_gastos_comunes")
        datos = {
            'form': ModificarGastoComunForm(instance=gasto_comun),
            'mensaje': "Modificado correctamente"
        }
    return render(request, 'core/modificar_gasto_comun.html', datos)

def res_espacios_comunes(request):
    rut_usuario = request.user.username  # Asumiendo que el nombre de usuario es el RUT
    # Filtrar los gastos comunes según el 'rut'
    residente = FichaResidente.objects.filter(rut=rut_usuario).first()
    res_espacio_comun = ReservaEspComun.objects.filter(id_residente__rut=residente.rut)

    datos = {
        'res_espacio_comun': res_espacio_comun
    }
    return render(request, 'core/res_espacios_comunes.html', datos)


def cancelarReservaEspacioComunRes(request, id):
    resEspacioComun = get_object_or_404(ReservaEspComun, id_reserva_esp_comun=id)
    if request.method == 'POST':
        # Cambiar el estado del espacio común a "eliminado"
        estado_eliminado = get_object_or_404(Estado_R_EC, id_est_r_ec=2)  # Get the Estado_EC instance with ID 4
        resEspacioComun.estado_reserva = estado_eliminado
        resEspacioComun.save()  # Guardar los cambios
        resEspacioComun = ReservaEspComun.objects.get(id_reserva_esp_comun=id)
        messages.success(request,"Espacio comun registrado correctamente")
        datos={}
        datos['mensaje'] = "Guardados Correctamente"
        rut_usuario = request.user.username  # Asumiendo que el nombre de usuario es el RUT
        # Filtrar los gastos comunes según el 'rut'
        residente = FichaResidente.objects.filter(rut=rut_usuario).first()
        contenido = "Le informamos que su reserva se ha sido cancelada\n\n Datos de reserva:\n Descripción : {} \n Fecha : {} \n Hora: {}\n Espacio común: {} \n Para revisar el detalle ingresar a la siguiente URL\n http://127.0.0.1:8000/res_espacios_comunes \nDesde ya muchas gracias.\nSaludos".format(resEspacioComun.descripcion,resEspacioComun.fecha,resEspacioComun.hora,resEspacioComun.id_espacio_comun)
        email = EmailMessage("Reservas HomeFun",
                             "Hola! {} :\n\n {}".format(residente.nombre, contenido),
                             '',
                             [residente.correo],
                             reply_to=[residente.correo])
        email.send()
        messages.success(request, "Reserva cancelada")
        return redirect(to="res_espacios_comunes")

    # En caso de que no sea una solicitud POST, se podría redirigir o mostrar un formulario
    return render(request, 'core/res_espacios_comunes.html', {
        'form': EspacioComunForm(instance=resEspacioComun)
    })

def modificar_res_espacio_comun_res(request, id):
    resEspacioComun = ReservaEspComun.objects.get(id_reserva_esp_comun=id)
    datos = {
        'form': ModReservaEspacioComunForm(instance=resEspacioComun)
    }
    if request.method == 'POST':
        formulario = ModReservaEspacioComunForm(data= request.POST, instance= resEspacioComun)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Reserva modificada correctamente")
            formulario.save()
            resEspacioComun = ReservaEspComun.objects.get(id_reserva_esp_comun=id)
            messages.success(request,"Espacio común modificado correctamente")
            datos['mensaje'] = "Guardados Correctamente"
            rut_usuario = request.user.username  # Asumiendo que el nombre de usuario es el RUT
            # Filtrar los gastos comunes según el 'rut'
            residente = FichaResidente.objects.filter(rut=rut_usuario).first()
            contenido = "Le informamos que su reserva se ha Modificado correctamente\n\n Datos de reserva:\n Descripción : {} \n Fecha : {} \n Hora: {}\n Espacio común: {} \n Para revisar el detalle ingresar a la siguiente URL\n http://127.0.0.1:8000/res_espacios_comunes \nDesde ya muchas gracias.\nSaludos".format(resEspacioComun.descripcion,resEspacioComun.fecha,resEspacioComun.hora,resEspacioComun.id_espacio_comun)
            email = EmailMessage("Reservas HomeFun",
                                 "¡Hola! {} :\n\n {}".format(residente.nombre, contenido),
                                 '',
                                 [residente.correo],
                                 reply_to=[residente.correo])
            email.send()
            return redirect(to="res_espacios_comunes")
        datos = {
            'form': ModReservaEspacioComunForm(instance=resEspacioComun),
            'mensaje': "Modificado correctamente"
        }

    return render(request, 'core/modificar_res_espacio_comun.html', datos)

def crear_res_espacio_comun_res(request):
    datos = {
        'form': CrearReservaEspacioComunResForm(user=request.user)  # Pasamos el usuario logueado al formulario
    }
    
    if request.method == 'POST':
        formulario = CrearReservaEspacioComunResForm(data=request.POST, user=request.user)  # Pasamos el usuario también aquí
        if formulario.is_valid():
            rut_usuario = request.user.username  # Asumiendo que el nombre de usuario es el RUT
            # Filtrar el residente usando el 'rut' del usuario
            residente = FichaResidente.objects.filter(rut=rut_usuario).first()
            
            if not residente:
                messages.error(request, "No se encontró una reserva asociada con este usuario.")
                return render(request, 'core/crear_res_espacio_comun_res.html', datos)
            
            # Asignar el residente a la reserva
            formulario.instance.id_residente = residente  # Asignamos el objeto FichaResidente a id_residente
            formulario.instance.estado_reserva = formulario.cleaned_data.get('estado_reserva')  # Si es necesario asignar el estado
            
            # Guardamos la reserva
            formulario.save()
            messages.success(request, "Reserva registrada correctamente")
            datos['mensaje'] = "Guardado correctamente"
            
            # Enviar correo al residente
            contenido = f"Le informamos que su reserva se ha realizado correctamente\n\n" \
                        f"Datos de reserva:\nDescripción: {formulario.cleaned_data['descripcion']}\nFecha: {formulario.cleaned_data['fecha']}\nHora: {formulario.cleaned_data['hora']}\nEspacio común: {formulario.cleaned_data['id_espacio_comun']}\n" \
                        "Para revisar el detalle, ingrese a la siguiente URL: http://127.0.0.1:8000/res_espacios_comunes\n" \
                        "¡Desde ya muchas gracias!\nSaludos"
            
            email = EmailMessage(
                "Reservas HomeFun",
                f"Hola! {residente.nombre} :\n\n {contenido}",
                '',
                [residente.correo],
                reply_to=[residente.correo]
            )
            email.send()

            # Redirigir a la página de reservas
            return redirect(to="res_espacios_comunes")
        else:
            print("Error: el formulario no es válido.")
            # Aquí puedes agregar un mensaje de error para el usuario si es necesario
    return render(request, 'core/crear_res_espacio_comun_res.html', datos)


def consulta_estado_cuenta(request):
    seleccionados_gc = request.session.get('seleccionados_gc', [])
    rut_usuario = request.user.username  # Asumiendo que el nombre de usuario es el RUT
    # Filtrar los gastos comunes según el 'rut'
    residente = FichaResidente.objects.filter(rut=rut_usuario).first()
    controler = Controller()

    

    if residente:
        gasto_comun = GastoComun.objects.filter(id_dpto__id_residente__rut=residente.rut)
        print(gasto_comun)
    else:
        gasto_comun = GastoComun.objects.none()

    datos = {
        'gasto_comun': gasto_comun,
        'seleccionados_gc': seleccionados_gc,
        'total_g': total_g,
    }
    preferencias = controler.pagar(datos['total_g'])

    try:
         url = ""
         url = str(request)
         aprovado="status=approved"
         if(aprovado in url):
             return redirect(to="panel_residente")
         else:
             print("No hay pago")
         print("la url es : " , url)
         preferencias = controler.pagar(total_g)
         datos['preference_id']=preferencias["response"]["id"]
         
    except:
         datos['mensaje'] = 'Error productos no encontrados'


    return render(request, 'core/consulta_estado_cuenta.html', datos)

def consulta_estado_multa(request):
    seleccionados = request.session.get('seleccionados', [])
    rut_usuario = request.user.username  # Asumiendo que el nombre de usuario es el RUT
    # Filtrar los gastos comunes según el 'rut'
    residente = FichaResidente.objects.filter(rut=rut_usuario).first()

    if residente:
        multa = Multa.objects.filter(id_dpto__id_residente__rut=residente.rut)
        print(multa)
    else:
        multa = Multa.objects.none()

   # Configurar Mercado Pago
    sdk = mercadopago.SDK("TEST-799766335101209-102200-dc91acd07d20881aa5b98b60bf6e8129-2049276181")  # Reemplaza con tu token de acceso
    preference_data = {
        "purpose": "wallet_purchase",
        "items": [
            {
                "title": "Gasto Común",
                "quantity": 1,
                "unit_price": 100,  # Asegúrate de que `total` sea un número válido
            }
        ]
    }

    # Crear preferencia en Mercado Pago
    try:
        preference_response = sdk.preference().create(preference_data)
        preference_id = preference_response["response"]["id"]
    except Exception as e:
        preference_id = None
        print(f"Error creando preferencia: {e}")

    datos = {
        'multa': multa,
        'seleccionados': seleccionados,
        'total': total,
        'preference_id': preference_id,  # Pasar el ID de la preferencia al template
    }

    return render(request, 'core/consulta_estado_multa.html', datos)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CasaDepto, Multa

@csrf_exempt
def agregarPagoMulta(request, id):
    if request.method == 'POST':
        try:
            # Obtener la multa específica
            multa = Multa.objects.get(id_multa=id)

            # Obtener el monto desde el objeto relacionado
            monto = multa.tipo.monto

            # Obtener la lista actual de seleccionados desde la sesión
            seleccionados = request.session.get('seleccionados', [])

            # Añadir la multa si no está ya en la lista
            if id not in seleccionados:
                seleccionados.append(id)
                request.session['seleccionados'] = seleccionados

            # Actualizar el total en la sesión
            total_actual = request.session.get('total', 0)
            request.session['total'] = total_actual + monto

            return JsonResponse({'total': request.session['total']}, status=200)
        except Multa.DoesNotExist:
            return JsonResponse({'error': 'Multa no encontrada'}, status=404)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def removerPagoMulta(request, id):
    if request.method == 'POST':
        try:
            # Obtener la multa específica
            multa = Multa.objects.get(id_multa=id)

            # Obtener el monto desde el objeto relacionado
            monto = multa.tipo.monto

            # Obtener la lista actual de seleccionados desde la sesión
            seleccionados = request.session.get('seleccionados', [])

            # Eliminar la multa de la lista
            if id in seleccionados:
                seleccionados.remove(id)
                request.session['seleccionados'] = seleccionados

            # Actualizar el total en la sesión
            total_actual = request.session.get('total', 0)
            request.session['total'] = max(0, total_actual - monto)  # Evitar negativos

            return JsonResponse({'total': request.session['total']}, status=200)
        except Multa.DoesNotExist:
            return JsonResponse({'error': 'Multa no encontrada'}, status=404)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def modificar_morosidad(request, id):
    gasto_comun = GastoComun.objects.get(id_gc=id)
    datos = {
        'form': ModificarGastoComunForm(instance=gasto_comun)
    }
    if request.method == 'POST':
        formulario = ModificarGastoComunForm(data= request.POST, instance= gasto_comun)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Morosidad modificada correctamente")
            return redirect(to="visualizar_morosidad")
        datos = {
            'form': ModificarGastoComunForm(instance=gasto_comun),
            'mensaje': "Modificado correctamente"
        }
    return render(request, 'core/modificar_tipo_gasto_comun.html', datos)

def admin_departamento(request):
    dept = CasaDepto.objects.all()
    datos={
        'dept':dept,
    }
    return render(request,'core/admin_departamento.html',datos)

def modificar_departamento(request, id):
    depto = CasaDepto.objects.get(id_dpto=id)
    datos = {
        'form': ModificarDepartamentoForm(instance=depto)
    }
    if request.method == 'POST':
        formulario = ModificarDepartamentoForm(data= request.POST, instance= depto)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Residente de departamento modificado correctamente")
            return redirect(to="admin_departamento")
        datos = {
            'form': ModificarDepartamentoForm(instance=depto),
            'mensaje': "Modificado correctamente"
        }

    return render(request, 'core/modificar_departamento.html', datos)

def perfil(request):
    rut_usuario = request.user.username
    residente = FichaResidente.objects.get(rut=rut_usuario)
    datos = {
        'form': ModificarFichaResidenteForm(instance=residente)
    }
    if request.method == 'POST':
        formulario = ModificarFichaResidenteForm(data= request.POST, instance= residente)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Información modificada correctamente")
            return redirect(to="panel_residente")
        datos = {
            'form': ModificarFichaResidenteForm(instance=residente),
            'mensaje': "Modificado correctamente"
        }
    return render(request, 'core/modificar_ficha_residente.html', datos)

def calcularGasto(request, id):
    gasto_comun = get_object_or_404(GastoComun, id_gc=id)
    if request.method == 'POST':
        # Aquí ya tenemos el objeto 'tipo' directamente desde la relación
        tipo = gasto_comun.tipo  # Esto te da directamente la instancia de TipoGastoComun
        print(tipo)
        
        # Realizar el cálculo del total
        total_calculo = (tipo.monto * tipo.reajuste) * gasto_comun.consumo
        gasto_comun.total = total_calculo
        gasto_comun.save() 
        
        messages.success(request, "Tipo de gasto común activado")
        return redirect(to="admin_gastos_comunes")
    
    return render(request, 'core/admin_gastos_comunes.html', {
        'form': CrearGastoComunForm(instance=gasto_comun)
    })
