# django-cron-jobs/Dockerfile
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gettext \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de requerimientos
COPY requirements.txt /app/requirements.txt

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Copiar script de espera
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Cargar la configuración de entorno desde archivo .env
ENV DJANGO_SETTINGS_MODULE=phs_main_django.settings
ARG ENV
ENV ENV=${ENV}

# Exponer el puerto que usa Gunicorn
EXPOSE 8000

# Comando para correr en el contenedor (por defecto Gunicorn)
CMD ["gunicorn", "phs_main_django.wsgi:application", "--bind", "0.0.0.0:8000"]
