# Dockerfile

# Imagen base de Python
FROM python:3.12-slim

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wget \
    netcat-openbsd \
    bash \
    postgresql-client \
    gosu \
    && rm -rf /var/lib/apt/lists/*

# Crear un usuario y grupo no root
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Descargar Dockerize
RUN wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz \
    && rm dockerize-linux-amd64-v0.6.1.tar.gz

# Copiar el archivo de requerimientos
COPY requirements.txt /app/requirements.txt

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código al contenedor
COPY . /app

# Copiar el script de entrada y hacerlo ejecutable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Exponer el puerto
EXPOSE 8000

# Establecer el entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando por defecto
CMD ["gunicorn", "--bind", ":8000", "phs_main_django.wsgi:application"]
