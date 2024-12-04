# community_posts/admin.py

from django.contrib import admin
from .models import Community, Post
from django.utils.safestring import mark_safe
from django.utils import timezone
import pytz

class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'community_id', 'creator')
    readonly_fields = ('creator',)

    def has_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.creator == request.user
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.creator == request.user
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

class PostAdmin(admin.ModelAdmin):
    list_display = ('community', 'content', 'status', 'scheduled_time', 'author')
    readonly_fields = ('scheduled_time_info', 'author')

    def scheduled_time_info(self, obj=None):
        # Obtener las horas en Buenos Aires y Madrid con información de la zona horaria
        buenos_aires_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        madrid_tz = pytz.timezone('Europe/Madrid')

        buenos_aires_time = timezone.now().astimezone(buenos_aires_tz)
        madrid_time = timezone.now().astimezone(madrid_tz)

        buenos_aires_time_str = buenos_aires_time.strftime('%Y-%m-%d %H:%M:%S')
        madrid_time_str = madrid_time.strftime('%Y-%m-%d %H:%M:%S')
        buenos_aires_offset = buenos_aires_time.strftime('%z')
        madrid_offset = madrid_time.strftime('%z')

        # Mensaje a mostrar en el admin
        message = f"""
            <div style="margin-top: 15px;">
                <strong>Argentina time (GMT{buenos_aires_offset}):</strong> {buenos_aires_time_str}<br>
                <strong>Spain time (GMT{madrid_offset}):</strong> {madrid_time_str}<br><br>
                <em>La hora que seleccionás para programar la publicación es la que figura como "Spain time".</em>
            </div>
        """
        return mark_safe(message)

    scheduled_time_info.short_description = "Información sobre las zonas horarias"

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            readonly_fields += ['status']
        return readonly_fields

    def has_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.author == request.user
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.author == request.user
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Community, CommunityAdmin)
admin.site.register(Post, PostAdmin)
