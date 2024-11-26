# Ruta: community_posts/check_pending_posts.py

from .utils.puppeteer_publish import execute_publish_script
from .utils.post_status_manager import update_post_status
from .models import Post
from django.utils import timezone
from .utils.logger_util import setup_logger

def check_pending_posts():
    logger = setup_logger("check_pending_posts")

    now = timezone.now()
    pending_posts = Post.objects.filter(status__in=['pending', 'error', 'error-1', 'error-2', 'error-3', 'error-4'], scheduled_time__lte=now)

    for post in pending_posts:
        try:
            logger.info(f"Procesando post: {post.content}")
            success = execute_publish_script(post, logger)
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
