from rest_framework import serializers
from .models import UserPosts, UserProfile
from drf_extra_fields.fields import Base64ImageField


class UserPostSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True, required=False, read_only=True)
    class Meta:
        model = UserPosts
        fields = (
            'image', 'title', 'id', 'user',
        )

    def create(self, validated_data):
        try:
            image_data = validated_data.pop('image')
        except:
            image_data = None
        breakpoint()
        if 'title' in validated_data or 'image' in validated_data:
            return UserPosts.objects.create(**validated_data)
        raise serializers.ValidationError("There are nothing to send")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'user', 'status', 'image', 'id'
        )

    def update(self, instance, validated_data):

        if 'image' in validated_data:
            instance.image = validated_data['image']
        if 'status' in validated_data:
            instance.status = validated_data['status']
        instance.save()
        return instance



