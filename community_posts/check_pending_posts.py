import os
import django
import sys

# Configuración de Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phs_main_django.settings')
django.setup()

from django.utils import timezone
from community_posts.models import Post

def check_pending_posts():
    now = timezone.now()
    pending_posts = Post.objects.filter(status='pending', scheduled_time__lte=now)

    for post in pending_posts:
        success = execute_publish_script(post)

        if success:
            post.status = 'published'
        else:
            post.status = 'error'

        post.save()

def execute_publish_script(post):
    # Aquí iría la lógica para publicar el mensaje en la plataforma
    # Por ahora podemos simular el resultado de la publicación
    print(f"Intentando publicar el post: {post}")
    return True  # Simular éxito (o False para simular un error)

if __name__ == "__main__":
    check_pending_posts()
