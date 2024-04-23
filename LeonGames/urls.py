from django.urls import path
from .views import (WelcomeView, JuegosView, AñadirJuegoView, EditarJuegoView,
EliminarJuegoView, RegistroView, LogInView, LogOutView, CrearVenta, VentasView, EditarVentaView,
EliminarVentaView)
from django.contrib import admin

#Ponemos la urls que llevan los datos al template
urlpatterns = [
path('admin/', admin.site.urls),
path('', WelcomeView.as_view(), name='welcome'),
path('juegos/', JuegosView.as_view(), name='juegos'),
path('juegos/nuevoJuego', AñadirJuegoView.as_view(), name='nuevoJuego'),
path('juegos/editarJuego/<int:pk>/', EditarJuegoView.as_view(), name='editarJuego'),
path('juegos/eliminarJuego/<int:pk>/', EliminarJuegoView.as_view(), name='eliminarJuego'),
path('logIn/', LogInView.as_view(), name='login'),
path('logOut', LogOutView.as_view(), name='logout'),
path('registro/', RegistroView.as_view(), name='registro'),
path('ventas/', VentasView.as_view(), name='ventas'),
path('ventas/crearVenta/', CrearVenta.as_view(), name='crearVenta'),
path('ventas/editarVenta/<int:pk>/', EditarVentaView.as_view(), name='editarVenta'),
path('ventas/eliminarVenta/<int:pk>/', EliminarVentaView.as_view(), name='eliminarVenta'),
]