# Django Cron Jobs Project

Este proyecto está diseñado para gestionar publicaciones programadas en comunidades utilizando **Django**, **Celery**, **RabbitMQ** y **PostgreSQL**. La aplicación permite a las tutoras programar publicaciones que se ejecutarán automáticamente a la hora indicada, además de ofrecer una interfaz de administración a través de **Django Admin**.

## Tabla de Contenidos

- [Tecnologías Utilizadas](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
- [Estructura del Proyecto](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
    - [Archivos Clave](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
    - [Archivos de Configuración](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
- [Puertos Utilizados](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
    - [Script para Liberar Puertos en Linux](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
- [Flujo de Trabajo](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
- [Instalación](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
    - [Pre-requisitos](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
    - [Paso a Paso](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
- [Uso](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
- [Consideraciones Adicionales](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
    - [Seguridad](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
    - [Persistencia de Datos](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
    - [Variables de Entorno](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
- [Contribuciones](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
- [Licencia](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)
- [Enlaces de Interés](https://www.notion.so/12-11-24-README-md-13c257b1b7cb808fb255dc0f4037ffdc?pvs=21)

---

## Tecnologías Utilizadas

- **Django**: Framework web para el backend de la aplicación.
- **PostgreSQL**: Base de datos relacional para almacenar la información.
- **Celery**: Sistema de cola de tareas para gestionar procesos en segundo plano.
- **RabbitMQ**: Broker de mensajes utilizado por Celery.
- **Docker**: Contenedorización de todos los componentes para facilitar el despliegue.
- **Gunicorn**: Servidor WSGI para servir la aplicación Django en producción.
- **Selenium**: Automatización de tareas web para publicar en las comunidades.
- **WhiteNoise**: Sirve archivos estáticos en producción sin necesidad de un servidor web adicional.

---

## Estructura del Proyecto

### Archivos Clave

- **`community_posts/tasks.py`**
    - Define las tareas de Celery que se ejecutan en segundo plano.
- **`community_posts/check_pending_posts.py`**
    - Función que revisa los posts pendientes y los publica si es el momento adecuado.
- **`community_posts/utils/selenium_publish.py`**
    - Contiene el script de Selenium que automatiza el proceso de inicio de sesión y publicación.
- **`community_posts/utils/post_status_manager.py`**
    - Administra el estado de cada post después de cada intento de publicación, actualizando su estado según el resultado.
- **`community_posts/utils/logger_util.py`**
    - Configura y gestiona el registro de logs para monitorear los procesos y depurar errores.

### Archivos de Configuración

- **`phs_main_django/settings.py`**
    - Configuración principal de la aplicación Django.
    - **Claves Importantes**:
        - **`SECRET_KEY`**: Llave secreta de Django, se debe configurar con una variable de entorno.
        - **`DEBUG`**: Define si el modo debug está activo; debe ser `False` en producción.
        - **`ALLOWED_HOSTS`**: Lista de hosts permitidos; se debe configurar según el entorno.
        - **`DATABASES`**: Configuración de la base de datos; utiliza las variables de entorno definidas.
        - **`STATIC_URL`** y **`STATIC_ROOT`**: Configuración para servir archivos estáticos en producción con WhiteNoise.
        - **`CELERY_BROKER_URL`**: URL del broker de mensajes; se configura para usar RabbitMQ.
- **`.env`**
    - Archivo que contiene las variables de entorno utilizadas por el proyecto.
    - **Variables Importantes**:
        - **Base de Datos**:
            - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
        - **Django**:
            - `DJANGO_SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_PASSWORD`, `DJANGO_SUPERUSER_EMAIL`
        - **Celery**:
            - `CELERY_BROKER_URL`
        - **LearnWorlds API**:
            - `LW_API_KEY`, `LW_SECRET_KEY`, `LW_USERNAME`, `LW_PASSWORD`
- **`docker-compose.yml`**
    - Define los servicios de Docker que componen la aplicación.
    - **Servicios**:
        - **`web`**: Servicio de Django que utiliza Gunicorn.
        - **`celery_worker`**: Servicio que ejecuta los workers de Celery.
        - **`celery_beat`**: Servicio que programa las tareas periódicas con Celery Beat.
        - **`db`**: Servicio de base de datos PostgreSQL.
        - **`rabbitmq`**: Servicio de RabbitMQ para la cola de mensajes.
    - **Puertos Mapeados**:
        - **Web (Django)**: `8000:8000`
        - **RabbitMQ**:
            - **AMQP**: `5672:5672`
            - **Management**: `15672:15672`
        - **PostgreSQL**: `5432:5432`
- **`entrypoint.sh`**
    - Script de entrada que se ejecuta al iniciar los contenedores.
    - **Funciones**:
        - Espera a que la base de datos esté lista antes de iniciar el servicio.
        - Aplica migraciones de Django si corresponde.
        - Crea el superusuario de Django si no existe.
        - Ejecuta `collectstatic` para recopilar archivos estáticos.
        - Inicia el servicio proporcionado (Gunicorn, Celery Worker o Celery Beat).

---

## Puertos Utilizados

A continuación, se detallan todos los puertos utilizados en el proyecto:

- **8000**: Puerto en el que se expone la aplicación web de Django (Gunicorn).
- **5432**: Puerto utilizado por PostgreSQL.
- **5672**: Puerto AMQP utilizado por RabbitMQ para la comunicación con Celery.
- **15672**: Puerto de la interfaz de administración web de RabbitMQ.
- **15692**: Puerto utilizado por RabbitMQ para métricas de Prometheus (no mapeado en `docker-compose.yml`, pero puede ser relevante si se habilitan métricas).
- **6379**: Si se utiliza Redis en lugar de RabbitMQ (no en este caso), este sería el puerto por defecto.

**Nota**: Asegúrate de que estos puertos estén libres en tu máquina local o servidor para evitar conflictos durante las pruebas y el despliegue.

### Script para Liberar Puertos en Linux

Si deseas liberar los puertos mencionados que puedan estar en uso en tu sistema Linux, puedes utilizar el siguiente script. **ADVERTENCIA: Este script detendrá procesos en ejecución y puede ser peligroso si no se usa con precaución. Asegúrate de entender lo que hace antes de ejecutarlo.**

```bash
#!/bin/bash

# Lista de puertos a verificar
PUERTOS=(8000 5432 5672 15672 15692)

for PUERTO in "${PUERTOS[@]}"; do
  PID=$(sudo lsof -t -i :$PUERTO)
  if [ -n "$PID" ]; then
    echo "Deteniendo proceso en el puerto $PUERTO con PID $PID"
    sudo kill -9 $PID
  else
    echo "El puerto $PUERTO está libre."
  fi
done

```

Guarda este script en un archivo, por ejemplo, `liberar_puertos.sh`, dale permisos de ejecución y ejecútalo:

```
sh
Copy code
chmod +x liberar_puertos.sh
./liberar_puertos.sh

```

**Importante**: Ejecuta este script solo si estás seguro de que los procesos que se detendrán no son críticos para tu sistema. Detener procesos puede causar pérdida de datos o inestabilidad en el sistema.

---

## Flujo de Trabajo

1. **Creación de Usuario Tutor**:
    - Un usuario tutor se registra en la plataforma a través del panel de administración de Django o mediante la API.
    - Una vez registrado, el tutor puede iniciar sesión y acceder a la sección de publicaciones.
2. **Inicio de Sesión y Creación de Post Programado**:
    - El tutor inicia sesión en la plataforma y navega hasta la sección de comunidades.
    - Puede crear un post y definir una hora específica para su publicación (programación).
3. **Publicación Automática del Post**:
    - **Celery Beat** programa la ejecución periódica de la tarea `check_pending_posts_task`.
    - La función `check_pending_posts()` revisa las publicaciones pendientes y utiliza el script de Selenium (`execute_publish_script()`) para automatizar el proceso de publicación.
    - Si la publicación es exitosa, el estado del post se actualiza a `published`.
    - En caso de error, el estado se actualiza (por ejemplo, `error-1`, `error-2`, etc.) y el sistema reintenta hasta cinco veces antes de marcar el post como fallido (`error-00`).

---

## Instalación

### Pre-requisitos

- **Docker** y **Docker Compose** instalados en tu sistema.
- Crear un archivo `.env` en la raíz del proyecto basado en `.env.example` y configurar las variables necesarias.

### Paso a Paso

1. **Clonar el Repositorio**
    
    ```
    sh
    Copy code
    git clone https://github.com/ravioles33/django-cron-jobs.git
    cd django-cron-jobs
    
    ```
    
2. **Crear el Directorio de Configuración para RabbitMQ**
    
    ```
    sh
    Copy code
    mkdir rabbitmq
    
    ```
    
3. **Agregar el Archivo de Configuración de RabbitMQ**
    - Crea un archivo llamado `rabbitmq.conf` dentro del directorio `rabbitmq` con el contenido adecuado para configurar RabbitMQ según tus necesidades (si es necesario).
4. **Crear y Configurar el Archivo `.env`**
    - Copia el archivo `.env.example` a `.env`:
        
        ```
        sh
        Copy code
        cp .env.example .env
        
        ```
        
    - Edita el archivo `.env` y configura las variables de entorno según tus credenciales y entorno.
5. **Construir y Levantar los Contenedores**
    
    ```
    sh
    Copy code
    docker-compose up --build
    
    ```
    
    Esto construirá y lanzará los servicios definidos: Django, PostgreSQL, RabbitMQ, Celery Worker y Celery Beat.
    
6. **Acceder a la Aplicación**
    - **Aplicación Web (Django)**: [http://localhost:8000](http://localhost:8000/)
    - **Admin de Django**: http://localhost:8000/admin
        - **Usuario**: El definido en `DJANGO_SUPERUSER_USERNAME` en tu `.env` (por defecto `admin`).
        - **Contraseña**: La definida en `DJANGO_SUPERUSER_PASSWORD` en tu `.env` (por defecto `admin`).
    - **RabbitMQ Management**: [http://localhost:15672](http://localhost:15672/)
        - **Usuario**: `guest`
        - **Contraseña**: `guest`

---

## Uso

### Verificación de Servicios

Puedes verificar que los servicios están corriendo correctamente con:

```
sh
Copy code
docker ps

```

Para ver los logs de un servicio específico:

```
sh
Copy code
docker-compose logs web

```

### Interactuar con la Aplicación

- Navega a la aplicación web y prueba iniciar sesión con el superusuario.
- Puedes crear usuarios tutores y programar publicaciones desde el panel de administración o mediante la API (si está implementada).

---

## Consideraciones Adicionales

### Seguridad

- Los procesos se ejecutan con un usuario no root dentro de los contenedores para mejorar la seguridad.
- Asegúrate de cambiar las credenciales por defecto y utilizar valores seguros en producción.
- **No** compartas el archivo `.env` ni lo incluyas en el control de versiones.

### Persistencia de Datos

- El volumen `db_data` se utiliza para persistir los datos de PostgreSQL.
- Si deseas mantener los datos entre reinicios o actualizaciones, no elimines este volumen.

### Variables de Entorno

- Las variables sensibles y de configuración se almacenan en el archivo `.env`.
- Asegúrate de configurar correctamente las variables relacionadas con la base de datos, Django y otros servicios.
- **Variables Clave**:
    - `DJANGO_SECRET_KEY`: Debe ser una cadena aleatoria y secreta en producción.
    - `DEBUG`: Establece a `False` en producción.
    - `ALLOWED_HOSTS`: Lista de hosts permitidos; configura esto para evitar errores de host no válido.

---

## Contribuciones

¡Cualquier contribución al proyecto es bienvenida! Puedes hacer un fork del repositorio, realizar cambios y crear un pull request.

Pasos para contribuir:

1. Haz un fork del proyecto.
2. Crea una nueva rama para tu característica o bugfix:
    
    ```
    sh
    Copy code
    git checkout -b feature/nueva-funcionalidad
    
    ```
    
3. Realiza tus cambios y haz commits descriptivos.
4. Envía tus cambios al repositorio remoto:
    
    ```
    sh
    Copy code
    git push origin feature/nueva-funcionalidad
    
    ```
    
5. Crea un pull request desde tu repositorio fork al repositorio original.

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](https://www.notion.so/producthackers/LICENSE) para más detalles.

---

## Enlaces de Interés

- **Repositorio del Proyecto**: https://github.com/ravioles33/django-cron-jobs
- **Documentación de Django**: https://docs.djangoproject.com/
- **Documentación de Celery**: https://docs.celeryproject.org/
- **Documentación de RabbitMQ**: https://www.rabbitmq.com/documentation.html
- **Documentación de Docker**: https://docs.docker.com/

---

¡Gracias por usar este proyecto! Si tienes alguna pregunta o sugerencia, no dudes en abrir un issue en el repositorio.