# tutor_profile/admin.py

from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'lw_username')
    fields = ('user', 'lw_username', 'lw_password')

admin.site.register(UserProfile, UserProfileAdmin)
