# community_posts/apps.py

from django.apps import AppConfig

class CommunityPostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'community_posts'

    def ready(self):
        # Código para crear el grupo "Tutora" y asignar permisos
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from .models import Community, Post

        # Crear el grupo "Tutora" si no existe
        tutora_group, created = Group.objects.get_or_create(name='Tutora')

        # Obtener los permisos para Community
        community_content_type = ContentType.objects.get_for_model(Community)
        community_permissions = Permission.objects.filter(
            content_type=community_content_type,
            codename__in=[
                'view_community',
                'add_community',
                'change_community',
                'delete_community',
            ]
        )

        # Obtener los permisos para Post
        post_content_type = ContentType.objects.get_for_model(Post)
        post_permissions = Permission.objects.filter(
            content_type=post_content_type,
            codename__in=[
                'view_post',
                'add_post',
                'change_post',
                'delete_post',
            ]
        )

        # Asignar los permisos al grupo "Tutora"
        tutora_group.permissions.set(list(community_permissions) + list(post_permissions))
