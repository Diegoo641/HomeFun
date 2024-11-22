from django.shortcuts import render, redirect
from django.contrib import messages
#from .controller import Controller
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from core.form import CrearGastoComunForm, CrearMultaForm, CrearTipoMultaForm, GenerarMultaForm,CrearUsuario, CrearCuentaUsuario , EspacioComunForm, ModReservaEspacioComunForm, \
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
pagar=[]


def es_superusuario_o_staff(user):
    return user.is_superuser or user.is_staff

@login_required


def home(request):
    return render(request, 'core/home.html')

def inicio(request):
    return render(request, 'core/inicio.html')

def panel_admin(request):
    residentes = FichaResidente.objects.filter(estado_id=1)
    cant_activos = residentes.count()
    morosos = GastoComun.objects.filter(estado_gc=3).values('id_dpto__id_residente__rut').annotate(total_monto=Sum('total'))
    cant_morosos = morosos.count()
    reservas = (ReservaEspComun.objects
            .filter(estado_reserva=3)
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

def consulta_estado_cuenta(request):
    seleccionados = request.session.get('seleccionados', [])
    rut_usuario = request.user.username  # Asumiendo que el nombre de usuario es el RUT
    # Filtrar los gastos comunes según el 'rut'
    residente = FichaResidente.objects.filter(rut=rut_usuario).first()
    print(residente.rut)

    if residente:
        gasto_comun = GastoComun.objects.filter(id_dpto__id_residente__rut=residente.rut)
        print(gasto_comun)
    else:
        gasto_comun = GastoComun.objects.none()

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
        'gasto_comun': gasto_comun,
        'seleccionados': seleccionados,
        'total': total,
        'preference_id': preference_id,  # Pasar el ID de la preferencia al template
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
        messages.success(request,"Espacio comun registrado correctamente")
        residente = resEspacioComun.id_residente  # Esto te da acceso al objeto FichaResidente
        rut_residente = residente.rut
        descripcion = resEspacioComun.descripcion
        fecha = resEspacioComun.fecha
        hora = resEspacioComun.hora
        espacio_comun = resEspacioComun.id_espacio_comun
        # Filtrar los gastos comunes según el 'rut'
        residente = FichaResidente.objects.filter(rut=rut_residente).first()
        print(residente)
        contenido = "¡¡¡Le informamos que su reserva se cancelado!!!\n\n Datos de reserva:\n Descripcion : {} \n Fecha : {}\n Hora: {}\n Espacio comun: {} \n Para revisar el detalle ingresar a la siguiente URL\n http://127.0.0.1:8000/res_espacios_comunes \nDesde ya muchas gracias.\nSaludos".format(descripcion,fecha,hora,espacio_comun)
        email = EmailMessage("Reservas HomeFun",
                             "Hola! {} :\n\n {}".format(residente.nombre, contenido),
                             '',
                             [residente.correo],
                             reply_to=[residente.correo])
        email.send()
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
            reserva = formulario.save()
            messages.success(request,"Espacio comun registrado correctamente")
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
            contenido = "¡¡¡Le informamos que su reserva se ha modificado de manera correcta!!!\n\n Datos de reserva:\n Descripcion : {} \n Fecha : {}\n Hora: {}\n Espacio comun: {} \n Para revisar el detalle ingresar a la siguiente URL\n http://127.0.0.1:8000/res_espacios_comunes \nDesde ya muchas gracias.\nSaludos".format(descripcion,fecha,hora,espacio_comun)
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
            messages.success(request,"Espacio comun registrado correctamente")
            print(formulario)
            rut_residente = formulario.cleaned_data["descripcion"]
            descripcion = formulario.cleaned_data["descripcion"]
            fecha = formulario.cleaned_data["fecha"]
            hora = formulario.cleaned_data["hora"]
            espacio_comun = formulario.cleaned_data["id_espacio_comun"]
            datos['mensaje'] = "Guardados Correctamente"
            # Filtrar los gastos comunes según el 'rut'
            residente = FichaResidente.objects.filter(rut=rut_residente).first()
            print(residente)
            contenido = "¡¡¡Le informamos que su reserva se ha realizado de manera correcta!!!\n\n Datos de reserva:\n Descripcion : {} \n Fecha : {}\n Hora: {}\n Espacio comun: {} \n Para revisar el detalle ingresar a la siguiente URL\n http://127.0.0.1:8000/res_espacios_comunes \nDesde ya muchas gracias.\nSaludos".format(descripcion,fecha,hora,espacio_comun)
            email = EmailMessage("Reservas HomeFun",
                                 "Hola! {} :\n\n {}".format(residente.nombre, contenido),
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
            contenido = "¡¡¡Le informamos que su reserva se ha creado su cuenta de manera correcya!!!\n\n Datos de cueta:\n Nombre usuario : {} \n Pass : {}\n  Para ingresar al sistema ingrese a la siguiente URL\n http://127.0.0.1:8000/accounts/login/ \nDesde ya muchas gracias.\nSaludos".format(usuario.username,password)
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
            messages.success(request,"Cuenta creada correctamente")
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
        estado_activado = get_object_or_404(Estado_T_GC, id_est_t_gc=1)  
        gasto_comun.estado_t_gc = estado_activado
        gasto_comun.save() 
        messages.success(request, "Tipo de gasto comu activado")
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
            messages.success(request, "Multa modificada correctamente")
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
        messages.success(request, "Tipo de gasto comu desactivado")
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
        messages.success(request, "Tipo de gasto comu activado")
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
            messages.success(request,"Cuenta creada correctamente")
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
        formulario = ModificarMultaForm(data= request.POST, instance= tipo_multa)
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
        messages.success(request, "Tipo de gasto comu activado")
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
            # Obtener la lista actual de seleccionados desde la sesión
            seleccionados = request.session.get('seleccionados', [])
            
            # Añadir el gasto si no está en la lista
            if id not in seleccionados:
                seleccionados.append(id)
                request.session['seleccionados'] = seleccionados
                
            total_actual = request.session.get('total', 0)
            request.session['total'] = total_actual + gasto.total
            return JsonResponse({'total': request.session['total']}, status=200)
        except GastoComun.DoesNotExist:
            return JsonResponse({'error': 'Gasto no encontrado'}, status=404)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def removerPago(request, id):
    if request.method == 'POST':
        try:
            gasto = GastoComun.objects.get(id_gc=id)
            # Obtener la lista actual de seleccionados desde la sesión
            seleccionados = request.session.get('seleccionados', [])
            
            # Eliminar el gasto de la lista
            if id in seleccionados:
                seleccionados.remove(id)
                request.session['seleccionados'] = seleccionados
            
            total_actual = request.session.get('total', 0)
            request.session['total'] = max(0, total_actual - gasto.total)  # Evitar negativos
            return JsonResponse({'total': request.session['total']}, status=200)
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
            messages.success(request,"Tipo de gasto comun creado correctamente")
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
        messages.success(request, "Tipo de gasto comu desactivado")
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
        messages.success(request, "Tipo de gasto comun activado")
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
            messages.success(request, "Gasto comun modificada correctamente")
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
            messages.success(request, "Multa modificada correctamente")
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
        contenido = "¡¡¡Le informamos que su reserva se ha sido cancelada!!!\n\n Datos de reserva:\n Descripcion : {} \n Fecha : {} \n Hora: {}\n Espacio comun: {} \n Para revisar el detalle ingresar a la siguiente URL\n http://127.0.0.1:8000/res_espacios_comunes \nDesde ya muchas gracias.\nSaludos".format(resEspacioComun.descripcion,resEspacioComun.fecha,resEspacioComun.hora,resEspacioComun.id_espacio_comun)
        email = EmailMessage("Reservas HomeFun",
                             "Hola! {} :\n\n {}".format(residente.nombre, contenido),
                             '',
                             [residente.correo],
                             reply_to=[residente.correo])
        email.send()
        messages.success(request, "Espacio Común Eliminado")
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
            messages.success(request,"Espacio comun registrado correctamente")
            datos['mensaje'] = "Guardados Correctamente"
            rut_usuario = request.user.username  # Asumiendo que el nombre de usuario es el RUT
            # Filtrar los gastos comunes según el 'rut'
            residente = FichaResidente.objects.filter(rut=rut_usuario).first()
            contenido = "¡¡¡Le informamos que su reserva se ha Modificado de manera correcta!!!\n\n Datos de reserva:\n Descripcion : {} \n Fecha : {} \n Hora: {}\n Espacio comun: {} \n Para revisar el detalle ingresar a la siguiente URL\n http://127.0.0.1:8000/res_espacios_comunes \nDesde ya muchas gracias.\nSaludos".format(resEspacioComun.descripcion,resEspacioComun.fecha,resEspacioComun.hora,resEspacioComun.id_espacio_comun)
            email = EmailMessage("Reservas HomeFun",
                                 "Hola! {} :\n\n {}".format(residente.nombre, contenido),
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
        'form': CrearReservaEspacioComunForm()
    }
    if request.method == 'POST':
        formulario = CrearReservaEspacioComunForm(data= request.POST)
        if formulario.is_valid():
            formulario.cleaned_data["estado_reserva"]
            descripcion = formulario.cleaned_data["descripcion"]
            fecha = formulario.cleaned_data["fecha"]
            hora = formulario.cleaned_data["hora"]
            espacio_comun = formulario.cleaned_data["id_espacio_comun"]

            formulario.save()
            messages.success(request,"Espacio comun registrado correctamente")
            datos['mensaje'] = "Guardados Correctamente"
            rut_usuario = request.user.username  # Asumiendo que el nombre de usuario es el RUT
            # Filtrar los gastos comunes según el 'rut'
            residente = FichaResidente.objects.filter(rut=rut_usuario).first()
            contenido = "¡¡¡Le informamos que su reserva se ha realizado de manera correcta!!!\n\n Datos de reserva:\n Descripcion : {} \n Fecha : {}\n Hora: {}\n Espacio comun: {} \n Para revisar el detalle ingresar a la siguiente URL\n http://127.0.0.1:8000/res_espacios_comunes \nDesde ya muchas gracias.\nSaludos".format(descripcion,fecha,hora,espacio_comun)
            email = EmailMessage("Reservas HomeFun",
                                 "Hola! {} :\n\n {}".format(residente.nombre, contenido),
                                 '',
                                 [residente.correo],
                                 reply_to=[residente.correo])
            email.send()
            return redirect(to="res_espacios_comunes")
        else:
            print("Error")
    return render(request, 'core/crear_res_espacio_comun.html',datos)  



def consulta_estado_multa(request):
    seleccionados = request.session.get('seleccionados', [])
    rut_usuario = request.user.username  # Asumiendo que el nombre de usuario es el RUT
    # Filtrar los gastos comunes según el 'rut'
    residente = FichaResidente.objects.filter(rut=rut_usuario).first()
    print(residente.rut)

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
            messages.success(request, "Gasto comun modificada correctamente")
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
            messages.success(request, "Multa modificada correctamente")
            return redirect(to="admin_departamento")
        datos = {
            'form': ModificarDepartamentoForm(instance=depto),
            'mensaje': "Modificado correctamente"
        }

    return render(request, 'core/modificar_departamento.html', datos)
