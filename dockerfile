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
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Instalar Puppeteer
RUN npm install -g puppeteer-extra puppeteer puppeteer-extra-plugin-stealth

# Crear un usuario y grupo no root con directorio home
RUN addgroup --system appgroup && adduser --system --ingroup appgroup --home /home/appuser --disabled-password appuser

# Establecer el directorio home y permisos adecuados
WORKDIR /app

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
