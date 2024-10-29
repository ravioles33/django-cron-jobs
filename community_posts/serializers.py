from rest_framework import serializers
from .models import Community, Post

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'community_id']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'community', 'content', 'status', 'scheduled_time']