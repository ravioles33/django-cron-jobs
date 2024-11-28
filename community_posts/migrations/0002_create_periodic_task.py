from django.db import migrations

def create_periodic_task(apps, schema_editor):
    PeriodicTask = apps.get_model('django_celery_beat', 'PeriodicTask')
    IntervalSchedule = apps.get_model('django_celery_beat', 'IntervalSchedule')

    # Crear o obtener el intervalo de 5 minutos
    interval, created = IntervalSchedule.objects.get_or_create(
        every=5,
        period=IntervalSchedule.MINUTES,
    )

    # Crear la tarea periódica si no existe
    PeriodicTask.objects.update_or_create(
        name='check_pending_posts_every_5_minutes',
        defaults={
            'interval': interval,
            'task': 'community_posts.tasks.check_pending_posts_task',
            'enabled': True,
        }
    )

class Migration(migrations.Migration):

    dependencies = [
        ('community_posts', '0001_initial'),
        ('django_celery_beat', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_periodic_task),
    ]
