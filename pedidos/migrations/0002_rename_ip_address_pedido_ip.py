# Generated by Django 5.1.1 on 2024-10-14 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedido',
            old_name='ip_address',
            new_name='ip',
        ),
    ]
