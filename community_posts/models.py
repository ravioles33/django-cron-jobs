from django.db import models

class Community(models.Model):
    name = models.CharField(max_length=255)
    community_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = (
        ('published', 'Publicado'),
        ('pending', 'Pendiente'),
        ('error', 'Error'),
    )

    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    scheduled_time = models.DateTimeField()

    def __str__(self):
        return f"{self.community.name} - {self.status}"