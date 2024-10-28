from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lw_username = models.CharField(max_length=150, blank=True, null=True)
    lw_password = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.user.username