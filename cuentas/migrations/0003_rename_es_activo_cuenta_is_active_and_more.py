# Generated by Django 5.1.1 on 2024-10-05 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0002_alter_cuenta_es_activo_alter_cuenta_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cuenta',
            old_name='es_activo',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='cuenta',
            old_name='es_admin',
            new_name='is_admin',
        ),
        migrations.RenameField(
            model_name='cuenta',
            old_name='es_staff',
            new_name='is_staff',
        ),
        migrations.RenameField(
            model_name='cuenta',
            old_name='es_superadmin',
            new_name='is_superadmin',
        ),
    ]
