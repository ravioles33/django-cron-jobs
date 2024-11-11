#!/bin/bash
set -e

# Esperar a que la base de datos esté lista
echo "Esperando a que la base de datos esté lista..."
dockerize -wait tcp://$DB_HOST:$DB_PORT -timeout 60s

# Comprobar si la base de datos existe y crearla si es necesario
echo "Verificando si la base de datos '$DB_NAME' existe..."
RESULT=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")
if [ "$RESULT" != "1" ]; then
    echo "La base de datos '$DB_NAME' no existe. Creándola..."
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -c "CREATE DATABASE \"$DB_NAME\""
    echo "Base de datos '$DB_NAME' creada."
fi

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py migrate

# Ejecutar el comando proporcionado
echo "Iniciando el servicio con el comando: $@"
exec "$@"
