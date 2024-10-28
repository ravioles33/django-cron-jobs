from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Community(models.Model):
    name = models.CharField(max_length=255)
    community_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('published', 'Publicado'),
        ('error', 'Error')
    ]

    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scheduled_time = models.DateTimeField()

    def clean(self):
        # Asegúrate de que la hora de publicación no esté en el pasado
        if self.scheduled_time < timezone.now():
            raise ValidationError('La fecha y hora de publicación no pueden estar en el pasado.')

    def save(self, *args, **kwargs):
        # Llama a clean() para realizar la validación antes de guardar
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Post to {self.community.name} at {self.scheduled_time} - Status: {self.status}"
