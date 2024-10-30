import os
import django
import sys

# Configuración de Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phs_main_django.settings')
django.setup()

from django.utils import timezone
from community_posts.models import Post
from community_posts.tasks import execute_publish_script

def check_pending_posts():
    now = timezone.now()
    pending_posts = Post.objects.filter(status='pending', scheduled_time__lte=now)

    for post in pending_posts:
        success = execute_publish_script(post)

        if success:
            post.status = 'published'
        else:
            if "error-" in post.status:
                current_attempt = int(post.status.split('-')[1])
                if current_attempt < 5:
                    post.status = f'error-{current_attempt + 1}'
                else:
                    post.status = 'error-00'
            else:
                post.status = 'error-1'

        post.save()

if __name__ == "__main__":
    check_pending_posts()
