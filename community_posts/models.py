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
        ('error', 'Error'),
        ('error-1', 'Error - Intento 1'),
        ('error-2', 'Error - Intento 2'),
        ('error-3', 'Error - Intento 3'),
        ('error-4', 'Error - Intento 4'),
        ('error-5', 'Error - Intento 5'),
        ('error-00', 'Error - Sin reintentos disponibles')
    ]

    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scheduled_time = models.DateTimeField()

    def clean(self):
        # Asegúrate de que la hora de publicación no esté en el pasado solo si el estado es 'pending'
        if self.status == 'pending' and self.scheduled_time < timezone.now():
            raise ValidationError('La fecha y hora de publicación no pueden estar en el pasado.')

    def save(self, *args, **kwargs):
        # Llama a clean() para realizar la validación antes de guardar
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Post to {self.community.name} at {self.scheduled_time} - Status: {self.status}"

    def retry_publication(self):
        if self.status.startswith('error') and self.status != 'error-00':
            current_attempt = int(self.status.split('-')[-1]) if '-' in self.status else 0
            if current_attempt < 5:
                self.status = f'error-{current_attempt + 1}'
            else:
                self.status = 'error-00'
            self.save()
