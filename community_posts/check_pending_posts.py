# community_posts/check_pending_posts.py

import subprocess
import json
from .utils.post_status_manager import update_post_status
from .models import Post
from django.utils import timezone
from .utils.logger_util import setup_logger
from django.conf import settings
from tutor_profile.models import UserProfile

def execute_publish_script(post, lw_username, lw_password, logger):
    """
    Ejecuta el script puppeteer_publish.js usando Node.js para publicar un post.
    """
    try:
        # Convertir el contenido y otros datos del post a JSON
        post_data = {
            "community_id": post.community.community_id,
            "content": post.content,
            "lw_username": lw_username,
            "lw_password": lw_password,
        }

        # Ejecutar el archivo puppeteer_publish.js como un proceso externo
        result = subprocess.run(
            ['node', 'community_posts/utils/puppeteer_publish.js'],
            input=json.dumps(post_data),
            text=True,
            capture_output=True
        )

        # Registrar la salida del script
        logger.info(f"Puppeteer script output: {result.stdout}")
        if result.stderr:
            logger.error(f"Puppeteer script error output: {result.stderr}")

        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error al ejecutar Puppeteer script: {str(e)}")
        return False

def check_pending_posts():
    """
    Revisa y procesa los posts pendientes.
    """
    logger = setup_logger("check_pending_posts")

    now = timezone.now()
    pending_posts = Post.objects.filter(
        status__in=['pending', 'error-1', 'error-2', 'error-3', 'error-4'],
        scheduled_time__lte=now
    )

    for post in pending_posts:
        try:
            logger.info(f"Procesando post: {post.content}")

            if post.author.is_superuser:
                lw_username = settings.LW_USERNAME
                lw_password = settings.LW_PASSWORD
            else:
                try:
                    profile = UserProfile.objects.get(user=post.author)
                    lw_username = profile.lw_username
                    lw_password = profile.lw_password
                    if not lw_username or not lw_password:
                        post.status = 'error-5'
                        post.save()
                        logger.warning(f"Credenciales de LW faltantes para el usuario {post.author.username}")
                        continue
                except UserProfile.DoesNotExist:
                    post.status = 'error-5'
                    post.save()
                    logger.warning(f"Perfil de usuario no encontrado para {post.author.username}")
                    continue

            success = execute_publish_script(post, lw_username, lw_password, logger)
            if success:
                post.status = 'published'
                logger.info(f"Publicado exitosamente: {post.content}")
            else:
                update_post_status(post, logger)
                logger.warning(f"Error al publicar: {post.content}, nuevo estado: {post.status}")
        except Exception as e:
            update_post_status(post, logger)
            logger.error(f"Error durante la publicación de {post.content}, Error: {str(e)}")

        post.save()
