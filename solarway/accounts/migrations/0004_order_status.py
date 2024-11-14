# Generated by Django 5.1.3 on 2024-11-14 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('cancelado', 'Cancelado'), ('en_proceso', 'En Proceso'), ('enviado', 'Enviado'), ('completado', 'Completado')], default='en_proceso', max_length=20),
        ),
    ]