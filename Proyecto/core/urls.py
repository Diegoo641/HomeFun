from django.urls import path, include
from core.views import home , registro,agregar_administrador, panel_admin


urlpatterns = [
    path('', home, name="home"),
    path('home', home, name="home"),
    path('registro',registro, name="registro"),
    path('agregar_administrador', agregar_administrador, name="agregar_administrador"),
    path('panel_admin', panel_admin, name="panel_admin"),
    



]
