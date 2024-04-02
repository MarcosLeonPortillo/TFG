from django.db import models

class Usuario(models.Model):
    Nombre = models.CharField(max_length=255)
    CorreoElectronico = models.CharField(max_length=255, unique=True)
    Contraseña = models.CharField(max_length=20)

    def __str__(self):
        return self.Nombre

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

class Juego(models.Model):
    Titulo = models.CharField(max_length=255)
    Genero = models.CharField(max_length=255, blank=True, null=True)
    Descripción = models.CharField(max_length=255, blank=True, null=True)
    Desarrollador = models.CharField(max_length=255, blank=True, null=True)
    Marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    Consola = models.ForeignKey(Consola, on_delete=models.CASCADE)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.Titulo

class Comentarios_juegos(models.Model):
    Juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    Texto = models.CharField(max_length=255)
    Fecha = models.CharField(max_length=255)

class Pedido(models.Model):
    Fecha = models.DateField()
    Comprador = models.ForeignKey(Usuario, related_name='comprador_pedidos', on_delete=models.CASCADE)
    Vendedor = models.ForeignKey(Usuario, related_name='vendedor_pedidos', on_delete=models.CASCADE)
    Juego = models.ForeignKey(Juego, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pedido ID: {self.id}"

class Pedido_juego(models.Model):
    Cantidad = models.IntegerField()
    Juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    Pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)

    def __str__(self):
        return f"Compra ID: {self.id}"
