from django.contrib import admin
from .models import Community, Post
from django.utils.safestring import mark_safe
import pytz
from datetime import datetime

class PostAdmin(admin.ModelAdmin):
    list_display = ('community', 'content', 'status', 'scheduled_time')
    readonly_fields = ('scheduled_time_info',)

    def scheduled_time_info(self, obj=None):
        # Obtén las horas en Buenos Aires y Madrid con información de la zona horaria
        buenos_aires_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        madrid_tz = pytz.timezone('Europe/Madrid')

        buenos_aires_time = datetime.now(buenos_aires_tz)
        madrid_time = datetime.now(madrid_tz)

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

admin.site.register(Community)
admin.site.register(Post, PostAdmin)
