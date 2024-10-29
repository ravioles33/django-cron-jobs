from celery import shared_task
from .models import Post
from django.utils import timezone

@shared_task
def check_pending_posts():
    now = timezone.now()
    pending_posts = Post.objects.filter(status='pending', scheduled_time__lte=now)

    for post in pending_posts:
        try:
            # Aquí podrías integrar tu script de Selenium para realizar la publicación.
            post.status = 'published'  # Actualiza el estado a 'publicado' si se hace correctamente
            print(f"Publicado: {post.content}")
        except Exception as e:
            post.status = 'error'  # Si falla, cambia el estado a 'error'
            print(f"Error al publicar: {post.content}, Error: {e}")

        post.save()
