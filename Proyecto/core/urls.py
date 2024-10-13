from django.urls import path, include
from core.views import home , inicio, registro,agregar_colaborador,agregar_administrador 


urlpatterns = [
    path('', inicio, name="inicio"),
    path('home', home, name="home"),
    path('inicio', inicio, name="inicio"),
    path('registro',registro, name="registro"),
    path('agregar_colaborador', agregar_colaborador, name="agregar_colaborador"),
    path('agregar_administrador', agregar_administrador, name="agregar_administrador"),
    



]
