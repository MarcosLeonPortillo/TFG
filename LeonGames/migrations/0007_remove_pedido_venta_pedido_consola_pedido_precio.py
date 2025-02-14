# Generated by Django 4.1.13 on 2024-05-20 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LeonGames', '0006_pedido_venta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='Venta',
        ),
        migrations.AddField(
            model_name='pedido',
            name='Consola',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='LeonGames.consola'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='Precio',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=10),
            preserve_default=False,
        ),
    ]
