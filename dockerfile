FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copiar archivo de requerimientos
COPY requirements.txt requirements.txt

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Configuración para producción o desarrollo
ARG ENV=development
ENV DJANGO_SETTINGS_MODULE=phs_main_django.settings.$ENV

# Exponer el puerto que usa Gunicorn
EXPOSE 8000

# Comando para correr en el contenedor (por defecto Gunicorn)
CMD ["gunicorn", "phs_main_django.wsgi:application", "--bind", "0.0.0.0:8000"]
