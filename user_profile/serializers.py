from rest_framework import serializers
from .models import UserPosts


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPosts
        fields = (
            'image', 'title', 'id', 'user'
        )

    def create(self, validated_data):
        if 'title' or 'image' in validated_data:
            return UserPosts.objects.create(**validated_data)


