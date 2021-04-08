from rest_framework import serializers
from rest_framework.fields import IntegerField, SerializerMethodField

from main.serializers import CurrentFriendsSerializer
from user.models import NewUser
from .models import UserPosts, UserProfile
from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from .services import get_friends, get_subscriptions, get_requested


class UserPostSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = UserPosts
        fields = (
            'image', 'title', 'id', 'user', 'likes'
        )

    def create(self, validated_data):
        if 'title' in validated_data or 'image' in validated_data:
            return UserPosts.objects.create(**validated_data)
        raise serializers.ValidationError("There are nothing to send")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'status', 'image', 'id'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image is not None:
            request = self.context['request']
            data['image'] = request.build_absolute_uri(instance.image.image.url)
        return data

    def update(self, instance, validated_data):

        if 'image' in validated_data:
            instance.image = validated_data['image']
        if 'status' in validated_data:
            instance.status = validated_data['status']
        instance.save()
        return instance


class UserProfileMySerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    friends = CurrentFriendsSerializer(many=True)
    subscriptions = CurrentFriendsSerializer(many=True)
    requested = CurrentFriendsSerializer(many=True)
    friends_count = IntegerField()

    class Meta:
        model = NewUser
        fields = (
            'username', 'profile', 'friends', 'subscriptions', 'requested', 'friends_count'
        )


class FriendOfFriendSerializer(CurrentFriendsSerializer):
    status = SerializerMethodField()

    class Meta(CurrentFriendsSerializer.Meta):
        fields = CurrentFriendsSerializer.Meta.fields + ('status',)

    def get_status(self, instance):
        main_user = self.context['main_user']
        friends = get_friends(main_user)
        subscriptions = get_subscriptions(main_user)
        requested = get_requested(main_user)
        if instance in friends:
            return "friend"
        elif instance in subscriptions:
            return "subscription"
        elif instance in requested:
            return "requested"
        return None


class UserProfileReadSerializer(UserProfileMySerializer):
    friends = FriendOfFriendSerializer(many=True)
    subscriptions = CurrentFriendsSerializer(many=True)
    requested = CurrentFriendsSerializer(many=True)
