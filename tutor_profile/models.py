# tutor_profile/models.py

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lw_username = models.CharField(max_length=255)
    lw_password = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s Profile"
