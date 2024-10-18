from django.urls import path, include
from core.views import home , registro,agregar_administrador, panel_admin, admin_espacios_comunes, eliminarEspacioComun, modificar_espacio_comun


urlpatterns = [
    path('', home, name="home"),
    path('home', home, name="home"),
    path('registro',registro, name="registro"),
    path('agregar_administrador', agregar_administrador, name="agregar_administrador"),
    path('admin_espacios_comunes', admin_espacios_comunes, name="admin_espacios_comunes"),
    path('panel_admin', panel_admin, name="panel_admin"),
    path('eliminarEspacioComun/<id>/',eliminarEspacioComun,name="eliminarEspacioComun"),
    path('modificar_espacio_comun/<id>/', modificar_espacio_comun, name='modificar_espacio_comun'),




]
