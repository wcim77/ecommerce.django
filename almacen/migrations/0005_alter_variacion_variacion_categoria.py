# Generated by Django 5.1.1 on 2024-10-08 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('almacen', '0004_remove_variacion_modelo_remove_variacion_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variacion',
            name='variacion_categoria',
            field=models.CharField(choices=[('modelo', 'modelo'), ('size', 'size')], max_length=100),
        ),
    ]
