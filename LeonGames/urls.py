from django.urls import path

from .views import (WelcomeView, JuegosView, AñadirJuegoView, EditarJuegoView,
EliminarJuegoView, RegistroView, LogInView, LogOutView, CrearVenta, VentasView, EditarVentaView,
EliminarVentaView, PerfilUsuarioView, EditarPerfilView, DetalleJuegoView, ComprarVentaView,
CrearComentarioView, EditarComentarioView, EliminarComentarioView, procesar_pedido,
compraExitosaView, chatView)
from django.conf import settings
from django.conf.urls.static import static
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
path('perfil/', PerfilUsuarioView.as_view(), name='perfil'),
path('perfil/editarPerfil', EditarPerfilView.as_view(), name='editarPerfil'),
path('detalleJuego/<int:pk>/', DetalleJuegoView.as_view(), name='detalleJuego'),
path('detalleJuego/comprarVenta/<int:venta_id>/', ComprarVentaView.as_view(), name='comprarVenta'),
path('procesar-pedido/', procesar_pedido, name='procesarPedido'),
path('detalleJuego/crearComentario/<int:pk>', CrearComentarioView.as_view(), name='crearComentario'),
path('detalleJuego/editarComentario/<int:pk>/', EditarComentarioView.as_view(), name='editarComentario'),
path('detalleJuego/eliminarComentario/<int:pk>/', EliminarComentarioView.as_view(), name='eliminarComentario'),
path('compraExitosa/', compraExitosaView.as_view(), name='compraExitosa'),
path('chat/', chatView.as_view(), name='chatbot'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)