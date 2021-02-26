from rest_framework import serializers
from .models import UserPosts, Likes


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPosts
        fields = (
            'image', 'title', 'id', 'user', 'likes'
        )

    def create(self, validated_data):
        if 'title' in validated_data or 'image' in validated_data:
            return UserPosts.objects.create(**validated_data)
        raise serializers.ValidationError("There are nothing to send")


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = (
            'user', 'post'
        )

    def create(self, validated_data):
        if 'title' in validated_data or 'image' in validated_data:
            return UserPosts.objects.create(**validated_data)
        raise serializers.ValidationError("There are nothing to send")


