# Dockerfile

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
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgcc1 \
    libgconf-2-4 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    lsb-release \
    xdg-utils \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Instalar Node.js 18.x
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Establecer variable de entorno para asegurar que Puppeteer descargue Chromium
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=false

# Instalar Dockerize si no está ya presente
RUN if ! command -v dockerize &> /dev/null; then \
    wget -qO /usr/local/bin/dockerize https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64 || \
    (echo "wget failed, trying curl" && curl -fsSL https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64 -o /usr/local/bin/dockerize); \
    chmod +x /usr/local/bin/dockerize; \
    fi

# Crear un usuario y grupo no root con directorio home
RUN addgroup --system appgroup && adduser --system --ingroup appgroup --home /home/appuser --disabled-password appuser

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos
COPY requirements.txt /app/requirements.txt

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos de dependencias Node.js
COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json

# Instalar las dependencias de Node.js y forzar la descarga de Chromium
RUN npm install --unsafe-perm=true

# Copiar el resto del código al contenedor
COPY . /app

# Ajustar permisos para el usuario appuser
RUN chown -R appuser:appgroup /app

# Copiar el script de entrada y hacerlo ejecutable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Cambiar al usuario appuser
USER appuser

# Exponer el puerto
EXPOSE 8000

# Establecer el entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando por defecto
CMD ["gunicorn", "--bind", ":8000", "phs_main_django.wsgi:application"]
