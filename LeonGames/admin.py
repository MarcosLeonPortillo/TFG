from django.contrib import admin
from .models import Usuario, Marca, Juego, Comentarios_juegos, Pedido, Pedido_juego

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Marca)
admin.site.register(Juego)
admin.site.register(Comentarios_juegos)
admin.site.register(Pedido)
admin.site.register(Pedido_juego)