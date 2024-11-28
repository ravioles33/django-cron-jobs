# community_posts/models.py

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User

class Community(models.Model):
    name = models.CharField(max_length=255)
    community_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('published', 'Publicado'),
        ('error-1', 'Error - Reintento 1'),
        ('error-2', 'Error - Reintento 2'),
        ('error-3', 'Error - Reintento 3'),
        ('error-4', 'Error - Reintento 4'),
        ('error-5', 'Error final - Sin reintentos disponibles')
    ]

    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scheduled_time = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        # Validar que la hora de publicación no esté en el pasado si el estado es 'pending'
        if self.status == 'pending' and self.scheduled_time < timezone.now():
            raise ValidationError('La fecha y hora de publicación no pueden estar en el pasado.')

    def save(self, *args, **kwargs):
        # Forzar estado a 'pending' solo al crear el post si el autor no es superusuario
        if not self.author.is_superuser and not self.pk:
            self.status = 'pending'
        # Llamar a clean() para realizar la validación antes de guardar
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Post to {self.community.name} at {self.scheduled_time} - Status: {self.status}"

    def retry_publication(self):
        error_statuses = ['error-1', 'error-2', 'error-3', 'error-4']
        if self.status in error_statuses:
            current_attempt = int(self.status.split('-')[-1])
            if current_attempt < 4:
                self.status = f'error-{current_attempt + 1}'
            else:
                self.status = 'error-5'
            self.save()
