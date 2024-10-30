# Generated by Django 5.1.2 on 2024-10-30 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community_posts', '0003_alter_post_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('pending', 'Pendiente'), ('published', 'Publicado'), ('error', 'Error'), ('error-1', 'Error - Intento 1'), ('error-2', 'Error - Intento 2'), ('error-3', 'Error - Intento 3'), ('error-4', 'Error - Intento 4'), ('error-5', 'Error - Intento 5'), ('error-00', 'Error - Sin reintentos disponibles')], default='pending', max_length=20),
        ),
    ]
