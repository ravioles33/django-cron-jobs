#!/bin/bash
set -e

# Esperar a que la base de datos esté lista
echo "Esperando a que la base de datos esté lista..."
dockerize -wait tcp://$DB_HOST:$DB_PORT -timeout 60s

if [ "$RUN_MIGRATIONS" = "true" ]; then
    # Comprobar si la base de datos existe y crearla si es necesario
    echo "Verificando si la base de datos '$DB_NAME' existe..."
    RESULT=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")
    if [ "$RESULT" != "1" ]; then
        echo "La base de datos '$DB_NAME' no existe. Creándola..."
        PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -c "CREATE DATABASE \"$DB_NAME\"" || echo "La base de datos '$DB_NAME' ya existe o ocurrió un error."
        echo "Base de datos '$DB_NAME' creada o ya existente."
    fi

    # Aplicar migraciones
    echo "Aplicando migraciones..."
    python manage.py migrate

    # Crear superusuario de Django si no existe
    echo "Creando superusuario de Django..."
    python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); \
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists(): \
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '', '$DJANGO_SUPERUSER_PASSWORD'); \
    print('Superusuario creado.'); \
else: \
    print('El superusuario ya existe.');"
fi

# Ejecutar el comando proporcionado
echo "Iniciando el servicio con el comando: $@"
exec "$@"
