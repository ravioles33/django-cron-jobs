# community_posts/apps.py

from django.apps import AppConfig

class CommunityPostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'community_posts'

    def ready(self):
        import community_posts.signals  # Importar las señales
