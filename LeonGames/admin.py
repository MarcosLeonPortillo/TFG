from django.contrib import admin
from .models import Venta, Marca, Juego, Comentarios_juegos, Pedido, Pedido_juego, Consola

# Register your models here.

admin.site.register(Venta)
admin.site.register(Marca)
admin.site.register(Juego)
admin.site.register(Comentarios_juegos)
admin.site.register(Pedido)
admin.site.register(Pedido_juego)
admin.site.register(Consola)