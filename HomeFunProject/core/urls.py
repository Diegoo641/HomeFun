from django.urls import path, include
from core.views import home , registro,agregar_administrador, modificar_res_espacio_comun,cancelarReservaEspacioComun,\
    panel_admin, admin_espacios_comunes, eliminarEspacioComun, modificar_espacio_comun, crear_espacio_comun, \
    habilitarEspacioComun,admin_res_espacios_comunes,consulta_estado_cuenta, panel_residente,crear_res_espacio_comun


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









]
