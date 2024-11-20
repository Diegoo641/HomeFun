from django.urls import path, include
from core.views import activarGastoComun, admin_departamento, agregarPagoMulta, cancelarReservaEspacioComunRes, consulta_estado_multa, crear_gasto_comun, crear_res_espacio_comun_res, desactivarGastoComun, home, modificar_departamento, modificar_gasto_comun, modificar_morosidad, modificar_res_espacio_comun_res , registro,agregar_administrador, modificar_res_espacio_comun,cancelarReservaEspacioComun,\
    panel_admin, admin_espacios_comunes, eliminarEspacioComun, modificar_espacio_comun, crear_espacio_comun, \
    habilitarEspacioComun,admin_res_espacios_comunes,consulta_estado_cuenta, panel_residente,crear_res_espacio_comun,\
    admin_cuentas,crear_cuenta,desactivarCuenta,activarCuenta, modificar_cuenta, admin_multas , modificar_multa ,\
    crear_multa,cancelarMulta,pagarMulta,eliminarMulta,admin_tipo_gasto_comun, admin_ficha_residentes, removerPagoMulta, res_espacios_comunes, visualizar_morosidad,\
    pagarDeuda,crear_tipo_gasto_comun,activarTipoGastoComun,desactivarTipoGastoComun, Multas, generar_multa,modificar_tipo_gasto_comun,\
    admin_ficha_residentes,modificar_ficha_residente,activarFichaResidente,desactivarFichaResidente,admin_tipo_multas,\
    crear_tipo_multa, modificar_tipo_multa, activarTipoMulta, desactivarTipoMulta, agregarPago,removerPago,admin_gastos_comunes


urlpatterns = [
    path('', home, name="home"),
    path('home', home, name="home"),
    path('registro',registro, name="registro"),
    path('agregar_administrador', agregar_administrador, name="agregar_administrador"),
    path('admin_espacios_comunes', admin_espacios_comunes, name="admin_espacios_comunes"),
    path('admin_res_espacios_comunes', admin_res_espacios_comunes, name="admin_res_espacios_comunes"),
    path('panel_admin', panel_admin, name="panel_admin"),
    path('eliminarEspacioComun/<id>/',eliminarEspacioComun,name="eliminarEspacioComun"),
    path('habilitarEspacioComun/<id>/',habilitarEspacioComun,name="habilitarEspacioComun"),
    path('modificar_espacio_comun/<id>/', modificar_espacio_comun, name='modificar_espacio_comun'),
    path('crear_espacio_comun', crear_espacio_comun, name="crear_espacio_comun"),
    path('cancelarReservaEspacioComun/<id>/',cancelarReservaEspacioComun,name="habilitarEspacioComun"),
    path('modificar_res_espacio_comun/<id>/', modificar_res_espacio_comun, name='modificar_res_espacio_comun'),
    path('consulta_estado_cuenta', consulta_estado_cuenta, name="consulta_estado_cuenta"),
    path('panel_residente',panel_residente, name="panel_residente"),
    path('crear_res_espacio_comun', crear_res_espacio_comun, name="crear_res_espacio_comun"),
    path('admin_cuentas', admin_cuentas, name="admin_cuentas"),
    path('crear_cuenta', crear_cuenta, name="crear_cuenta"),
    path('desactivarCuenta/<id>/',desactivarCuenta,name="desactivarCuenta"),
    path('activarCuenta/<id>/',activarCuenta,name="activarCuenta"),
    path('modificar_cuenta/<id>/', modificar_cuenta, name='modificar_cuenta'),
    path('admin_multas', admin_multas, name="admin_multas"),
    path('crear_multa', crear_multa, name="crear_multa"),
    path('modificar_multa/<id>/', modificar_multa, name="modificar_multa"),
    path('cancelarMulta/<id>/',cancelarMulta,name="cancelarMulta"),
    path('pagarMulta/<id>/',pagarMulta,name="pagarMulta"),
    path('eliminarMulta/<id>/',eliminarMulta,name="eliminarMulta"),
    path('admin_tipo_gasto_comun',admin_tipo_gasto_comun,name="admin_tipo_gasto_comun"),
    path('admin_ficha_residentes',admin_ficha_residentes,name="admin_ficha_residentes"),
    path('visualizar_morosidad',visualizar_morosidad,name="visualizar_morosidad"),
    path('pagarDeuda',pagarDeuda,name="pagarDeuda"),
    path('crear_tipo_gasto_comun', crear_tipo_gasto_comun, name="crear_tipo_gasto_comun"),
    path('activarTipoGastoComun/<id>/',activarTipoGastoComun,name="activarTipoGastoComun"),
    path('desactivarTipoGastoComun/<id>/',desactivarTipoGastoComun,name="desactivarTipoGastoComun"),
    path('Multas', Multas, name="Multas"),
    path('generar_multa',generar_multa,name="generar_multa"),
    path('modificar_tipo_gasto_comun/<id>/', modificar_tipo_gasto_comun, name="modificar_tipo_gasto_comun"),
    path('admin_ficha_residentes', admin_ficha_residentes, name="admin_ficha_residentes"),
    path('modificar_ficha_residente/<id>/', modificar_ficha_residente, name="modificar_ficha_residente"),
    path('activarFichaResidente/<id>/',activarFichaResidente,name="activarFichaResidente"),
    path('desactivarFichaResidente/<id>/',desactivarFichaResidente,name="desactivarFichaResidente"),
    path('admin_tipo_multas', admin_tipo_multas, name="admin_tipo_multas"),
    path('crear_tipo_multa', crear_tipo_multa, name="crear_tipo_multa"),
    path('modificar_tipo_multa/<id>/', modificar_tipo_multa, name="modificar_tipo_multa"),
    path('activarTipoMulta/<id>/',activarTipoMulta,name="activarTipoMulta"),
    path('desactivarTipoMulta/<id>/',desactivarTipoMulta,name="desaactivarTipoMulta"),
    path('agregar_pago/<int:id>/', agregarPago, name='agregar_pago'),
    path('remover_pago/<int:id>/', removerPago, name='remover_pago'),
    path('admin_gastos_comunes', admin_gastos_comunes, name="admin_gastos_comunes"),
    path('crear_gasto_comun', crear_gasto_comun, name="crear_gasto_comun"),
    path('activarGastoComun/<id>/',activarGastoComun,name="activarGastoComun"),
    path('desactivarGastoComun/<id>/',desactivarGastoComun,name="desactivarGastoComun"),
    path('modificar_gasto_comun/<id>/', modificar_gasto_comun, name="modificar_gasto_comun"),
    path('res_espacios_comunes', res_espacios_comunes, name="res_espacios_comunes"),
    path('cancelarReservaEspacioComunRes/<id>/',cancelarReservaEspacioComunRes,name="habilitarEspacioComun"),
    path('modificar_res_espacio_comun_res/<id>/', modificar_res_espacio_comun_res, name='modificar_res_espacio_comun'),
    path('crear_res_espacio_comun_res', crear_res_espacio_comun_res, name="crear_res_espacio_comun"),
    path('consulta_estado_multa', consulta_estado_multa, name="consulta_estado_multa"),
    path('agregar_pago_multa/<int:id>/', agregarPagoMulta, name='agregar_pago_multa'),
    path('remover_pago_multa/<int:id>/', removerPagoMulta, name='remover_pago_multa'),
    path('modificar_morosidad/<id>/', modificar_morosidad, name="modificar_morosidad"),
    path('admin_departamento', admin_departamento, name="admin_departamento"),
    path('modificar_departamento/<id>/', modificar_departamento, name="modificar_departamento"),























]
