from django.contrib.auth.models import User
from django.db import models

class Marca(models.Model):
    Nombre = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.Nombre

    class Meta:
        verbose_name_plural = "Marcas"

class Consola(models.Model):
    Nombre = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.Nombre

    class Meta:
        verbose_name_plural = "Consolas"


GENERO_CHOICES = [
    ('Acción', 'Acción'),
    ('Aventura', 'Aventura'),
    ('RPG', 'Rol (RPG)'),
    ('Disparos en primera persona', 'Disparos en primera persona (FPS)'),
    ('Disparos en tercera persona', 'Disparos en tercera persona (TPS)'),
    ('Plataforma', 'Plataforma'),
    ('Estrategia', 'Estrategia'),
    ('Simulación', 'Simulación'),
    ('Juego de cartas', 'Juego de cartas (Cartas)'),
    ('Estrategia en tiempo real', 'Estrategia en tiempo real (RTS)'),
    ('Horror', 'Horror'),
    ('Supervivencia', 'Supervivencia'),
    ('MMO', 'Multijugador masivo en línea (MMO)'),
    ('MOBA', 'Arena de batalla en línea multijugador (MOBA)'),
    ('Carreras', 'Carreras'),
    ('Lucha', 'Lucha'),
    ('Puzzle', 'Puzzle'),
    ('Novela visual', 'Novela visual (VN)'),
    ('Música', 'Música/Ritmo'),
    ('Deportes', 'Deportes'),
    ('Otro', 'Otro'),
]

class Juego(models.Model):
    Titulo = models.CharField(max_length=255)
    Genero = models.CharField(max_length=255, choices=GENERO_CHOICES)
    DescripcionJuego = models.CharField(max_length=255, blank=True, null=True)
    Desarrollador = models.CharField(max_length=255, blank=True, null=True)
    Lanzamiento = models.IntegerField(default=2024)
    Marca = models.ForeignKey(Marca, on_delete=models.CASCADE)

    def __str__(self):
        return self.Titulo

class Comentarios_juegos(models.Model):
    Juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    Usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    Texto = models.TextField(blank=True, null=True)
    Fecha = models.DateTimeField(auto_now_add=True)
    Valoracion = models.IntegerField(choices=[(1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')],
                                     blank=True,
                                     null=True)

    def get_valoracion(self):
        if self.valoracion:
            return '⭐' * self.valoracion
        else:
            return 'Sin valoración'


class Venta(models.Model):
    Juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    Vendedor = models.ForeignKey(User, related_name='vendedor_ventas', on_delete=models.CASCADE)
    Precio = models.DecimalField(max_digits=10, decimal_places=2)
    Fecha = models.DateField()
    DescripcionVenta = models.CharField(max_length=255, blank=True, null=True)
    Consola = models.ForeignKey(Consola, on_delete=models.CASCADE)

    def __str__(self):
        return f"Venta ID: {self.id}"

class Pedido(models.Model):
    Fecha = models.DateField()
    Comprador = models.ForeignKey(User, related_name='comprador_pedidos', on_delete=models.CASCADE)
    Vendedor = models.ForeignKey(User, related_name='vendedor_pedidos', on_delete=models.CASCADE)
    Juego = models.ForeignKey(Juego, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pedido ID: {self.id}"

class Pedido_juego(models.Model):
    Cantidad = models.IntegerField()
    Juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    Pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)

    def __str__(self):
        return f"Compra ID: {self.id}"
