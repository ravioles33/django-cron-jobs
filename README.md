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
- Crear un archivo `.env` en la raíz del proyecto basado en `.env.example` y configurar las variables necesarias.

### Paso a Paso de Instalación

1. **Clona el Repositorio**

   ```sh
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
Crear el Directorio de Configuración para RabbitMQ

sh
Copy code
mkdir rabbitmq
Agregar el Archivo de Configuración de RabbitMQ

Crea un archivo llamado rabbitmq.conf dentro del directorio rabbitmq con el contenido proporcionado anteriormente.
Construye y Levanta los Contenedores

sh
Copy code
docker-compose up --build
Esto construirá y lanzará los servicios definidos: Django, PostgreSQL, RabbitMQ, Celery Worker y Celery Beat.

Acceder a la Aplicación

Aplicación Web: http://localhost:8000
Admin de Django: http://localhost:8000/admin
Usuario: El definido en DJANGO_SUPERUSER_USERNAME en tu .env
Contraseña: La definida en DJANGO_SUPERUSER_PASSWORD en tu .env
RabbitMQ Management: http://localhost:15672
Usuario: guest
Contraseña: guest
Uso
Configuración de Entorno

El archivo .env determina el entorno del proyecto. Asegúrate de configurar todas las variables necesarias.
Tareas Programadas con Celery

Las tareas de Celery y Celery Beat se inician automáticamente con Docker Compose.
Verificación de Servicios

Puedes verificar que los servicios están corriendo correctamente con:

sh
Copy code
docker ps
Para ver los logs de un servicio específico:

sh
Copy code
docker-compose logs web
Consideraciones Adicionales
Seguridad

Los procesos se ejecutan con un usuario no root dentro de los contenedores para mejorar la seguridad.
Persistencia de Datos

El volumen db_data se utiliza para persistir los datos de PostgreSQL.
Variables de Entorno

Asegúrate de mantener las variables sensibles fuera del control de versiones y de no compartir el archivo .env.
Contribuciones
Cualquier contribución al proyecto es bienvenida. Puedes hacer un fork del repositorio, realizar cambios y crear un pull request.

Licencia
Este proyecto está bajo la licencia MIT.

markdown
Copy code

---

## Pasos Finales

Después de copiar y pegar todos los archivos en sus respectivos lugares:

1. **Crea el Directorio `rabbitmq` y Agrega `rabbitmq.conf`**

   - En la raíz de tu proyecto, crea un directorio llamado `rabbitmq`.
   - Dentro de este directorio, crea el archivo `rabbitmq.conf` con el contenido proporcionado.

2. **Actualiza el Archivo `.env`**

   - Asegúrate de que todas las variables en `.env` estén correctamente configuradas.

3. **Construye y Levanta los Contenedores**

   ```sh
   docker-compose up --build
Verifica el Funcionamiento

Accede a la aplicación web y verifica que puedes iniciar sesión con el superusuario de Django.
Revisa los logs para asegurarte de que no hay errores.
Confirma que las advertencias de RabbitMQ han desaparecido.
Verifica que los procesos no se están ejecutando como root dentro de los contenedores.