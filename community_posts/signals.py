# community_posts/signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Community, Post

@receiver(post_migrate)
def create_tutora_group(sender, **kwargs):
    if sender.name == 'community_posts':
        tutora_group, _ = Group.objects.get_or_create(name='Tutora')

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
