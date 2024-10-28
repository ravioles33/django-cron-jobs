from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommunityViewSet, PostViewSet

router = DefaultRouter()
router.register(r'communities', CommunityViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]