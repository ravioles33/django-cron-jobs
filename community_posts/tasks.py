# community_posts/tasks.py

from celery import shared_task
from .check_pending_posts import check_pending_posts

@shared_task
def check_pending_posts_task():
    check_pending_posts()
