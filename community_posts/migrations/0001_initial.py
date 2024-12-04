# Generated by Django 5.1.2 on 2024-12-04 18:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('community_id', models.CharField(max_length=100, unique=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('published', 'Publicado'), ('error-1', 'Error - Reintento 1'), ('error-2', 'Error - Reintento 2'), ('error-3', 'Error - Reintento 3'), ('error-4', 'Error - Reintento 4'), ('error-5', 'Error final - Sin reintentos disponibles')], default='pending', max_length=20)),
                ('scheduled_time', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community_posts.community')),
            ],
        ),
    ]