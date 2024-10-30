# Django Cron Jobs Project

Este proyecto está diseñado para gestionar publicaciones programadas en comunidades utilizando Django, Celery, RabbitMQ y PostgreSQL. La aplicación permite a las tutoras programar publicaciones que se ejecutarán automáticamente a la hora indicada, además de ofrecer una interfaz de administración a través de Django Admin.

## Tecnologías
- **Django**: Framework backend para gestionar la aplicación.
- **PostgreSQL**: Base de datos para almacenar la información.
- **Celery**: Gestión de tareas en segundo plano.
- **RabbitMQ**: Cola de mensajes para las tareas de Celery.
- **Docker**: Virtualización de todos los componentes.

## Estructura de Archivos

### Ubicaciones de Archivos Clave:
- **`tasks.py`**: `community_posts/tasks.py`
  - Define las tareas de Celery.
- **`check_pending_posts.py`**: `community_posts/check_pending_posts.py`
  - Revisa los posts pendientes y los publica si es posible.
- **`selenium_publish.py`**: `community_posts/utils/selenium_publish.py`
  - Contiene el script Selenium para la publicación.
- **`post_status_manager.py`**: `community_posts/utils/post_status_manager.py`
  - Administra el estado del post después de cada intento de publicación.
- **`logger_util.py`**: `community_posts/utils/logger_util.py`
  - Define la configuración de logs para registrar los procesos.

## Flujo de Trabajo

1. **Creación de Usuario Tutor**:
   - Un usuario tutor se registra en la plataforma a través del panel de administración de Django o utilizando la API.
   - Una vez registrado, el tutor puede iniciar sesión y acceder a la sección de publicaciones.

2. **Inicio de Sesión y Creación de Post Programado**:
   - El tutor se loguea en la plataforma y navega hasta la sección de comunidades.
   - Aquí puede crear un post y definir una hora específica para la publicación (es decir, se programa la publicación).

3. **Publicación Automática del Post**:
   - Celery ejecuta una tarea cada ciertos minutos que revisa las publicaciones pendientes (`check_pending_posts()`).
   - La función `check_pending_posts()` utiliza el script Selenium (`execute_publish_script()`) para iniciar sesión automáticamente, recuperar el token CSRF y hacer una solicitud a la API de publicación.
   - En caso de éxito, el estado del post se actualiza a `published`. Si falla, se actualiza el estado (`error`, `error-1`, etc.) y el sistema vuelve a intentarlo hasta cinco veces antes de darlo por fallido (`error-00`).

## Instalación
Para instalar y ejecutar el proyecto, sigue los siguientes pasos:

### Pre-requisitos
- Docker y Docker Compose instalados en tu sistema.
- Archivo `.env` en la raíz del proyecto con las siguientes configuraciones:

  ```
  LW_API_KEY=tu_api_key
  LW_SECRET_KEY=tu_secret_key
  DB_NAME=nombre_base_datos
  DB_USER=usuario_base_datos
  DB_PASSWORD=contraseña_base_datos
  DB_HOST=db
  DB_PORT=5432
  ENV=development  # Cambiar a 'production' para despliegue
  ```
  
- Cambia estos valores de ser necesario para tu entorno.

### Paso a Paso de Instalación
1. **Clona el Repositorio**
   ```sh
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
   ```

2. **Construye los Contenedores**
   ```sh
   docker-compose up --build
   ```

   Esto construirá y lanzará los servicios definidos: Django, PostgreSQL, RabbitMQ, Celery Worker, y Celery Beat.

3. **Migración de la Base de Datos**
   ```sh
   docker-compose exec web python manage.py migrate
   ```

4. **Crear Superusuario**
   ```sh
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Acceder a la Aplicación**
   - Admin de Django: [http://localhost:8000/admin](http://localhost:8000/admin)
   - RabbitMQ Management: [http://localhost:15672](http://localhost:15672) (usuario: `guest`, contraseña: `guest`)

### Uso
1. **Configuración de Entorno**
   El archivo `.env` determina el entorno del proyecto, puedes cambiar las configuraciones para `production` y `development`.

2. **Ejecutar Celery para las Tareas Programadas**
   - Ejecuta Celery Worker:
     ```sh
     docker-compose exec web celery -A phs_main_django worker --loglevel=info
     ```
   - Ejecuta Celery Beat:
     ```sh
     docker-compose exec web celery -A phs_main_django beat --loglevel=info
     ```

3. **Docker para Desarrollo y Producción**
   Cambia la variable de entorno `ENV` en el Dockerfile o `.env` para alternar entre entornos de desarrollo y producción.

## Notas
- **Redes**: Se configura una red interna para permitir la comunicación entre los servicios mientras que el acceso externo está limitado al puerto 8000 para Django y 15672 para RabbitMQ.
- **Volúmenes**: La persistencia de datos de PostgreSQL se maneja mediante volúmenes Docker.

## Consideraciones
Para despliegue en producción, asegúrate de:
- Usar un servidor WSGI más robusto (como Gunicorn, ya configurado en el Dockerfile).
- Configurar adecuadamente los ajustes de seguridad en Django (`DEBUG=False`, `ALLOWED_HOSTS`, etc).
- Implementar un servidor proxy inverso (por ejemplo, Nginx) para mejorar la seguridad y rendimiento.

## Contribuciones
Cualquier contribución al proyecto es bienvenida. Puedes hacer un fork del repositorio, realizar cambios y crear un pull request.

## Licencia
Este proyecto está bajo la licencia MIT.
