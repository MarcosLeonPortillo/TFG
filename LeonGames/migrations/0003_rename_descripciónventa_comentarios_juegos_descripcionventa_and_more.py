# Generated by Django 4.1.13 on 2024-04-20 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LeonGames', '0002_venta_alter_consola_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comentarios_juegos',
            old_name='DescripciónVenta',
            new_name='DescripcionVenta',
        ),
        migrations.RenameField(
            model_name='juego',
            old_name='DescripciónJuego',
            new_name='DescripcionJuego',
        ),
    ]
