from rest_framework import serializers
from user.models import NewUser
from .models import UserProfile, UserPosts


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'image',
        )

    def create(self, validated_data):
        userprofile = UserProfile(
            user=validated_data['user'],
            image=validated_data['image'],
        )
        return userprofile


