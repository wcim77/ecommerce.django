# Generated by Django 5.1.1 on 2024-10-07 05:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('almacen', '0002_alter_producto_precio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(max_length=50)),
                ('size', models.CharField(max_length=50)),
                ('variacion_categoria', models.CharField(choices=[('modelo', 'modelo'), ('size', 'size')], max_length=50)),
                ('valor_variacion', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.producto')),
            ],
        ),
    ]
