# Ruta: ./Dockerfile

# Dockerfile

# Imagen base de Python
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias necesarias para compilar librerías y herramientas necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wget \
    netcat-openbsd \
    bash \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Descargar Dockerize
RUN wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz \
    && rm dockerize-linux-amd64-v0.6.1.tar.gz

# Copiar el archivo de requerimientos
COPY requirements.txt /app/requirements.txt

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código al contenedor
COPY . .

# Copiar el script de entrada
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Comando por defecto para iniciar el servidor
CMD ["gunicorn", "--bind", ":8000", "phs_main_django.wsgi:application"]
