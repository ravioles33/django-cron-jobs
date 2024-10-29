from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Establecer el entorno de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phs_main_django.settings')

# Crear la instancia de Celery
app = Celery('phs_main_django')

# Cargar la configuración desde Django y ajustar Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-descubrimiento de tareas de aplicaciones instaladas
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.broker_connection_retry_on_startup = True
