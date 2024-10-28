from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tutor_profile/', include('tutor_profile.urls')),
    path('api/community_posts/', include('community_posts.urls')),
]