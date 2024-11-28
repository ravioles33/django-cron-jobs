# phs_main_django/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establecer el entorno de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phs_main_django.settings')

# Crear la instancia de Celery
app = Celery('phs_main_django')

# Cargar la configuración desde Django y ajustar Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-descubrimiento de tareas de aplicaciones instaladas
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# Configurar Celery Beat para usar el scheduler basado en la base de datos
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

# Asegurar que Celery reconecte al broker en caso de fallos al iniciar
app.conf.broker_connection_retry_on_startup = True

# Eliminar la configuración de beat_schedule para evitar conflictos
# from celery.schedules import crontab

# app.conf.beat_schedule = {
#     'check-pending-posts-every-5-minutes': {
#         'task': 'community_posts.tasks.check_pending_posts_task',
#         'schedule': crontab(minute='*/5'),
#     },
# }
