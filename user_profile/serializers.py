from django.contrib.auth.models import AnonymousUser
from rest_framework.fields import IntegerField, SerializerMethodField

from main.serializers import CurrentFriendsSerializer
from user.models import NewUser
from .models import UserPosts, UserProfile
from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from .services import get_friends, get_subscriptions, get_requested, friend_request_status


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
    relation = SerializerMethodField()

    class Meta(CurrentFriendsSerializer.Meta):
        fields = CurrentFriendsSerializer.Meta.fields + ('relation',)

    def get_relation(self, instance):
        main_user = self.context['main_user']
        # breakpoint()
        if not isinstance(main_user, AnonymousUser):
            return friend_request_status(main_user, get_friends(instance), get_subscriptions(instance),
                                         get_requested(instance))
        return None


class UserProfileReadSerializer(UserProfileMySerializer):
    friends = FriendOfFriendSerializer(many=True)
    subscriptions = FriendOfFriendSerializer(many=True)
    requested = FriendOfFriendSerializer(many=True)
    relation = SerializerMethodField()

    class Meta(UserProfileMySerializer.Meta):
        fields = UserProfileMySerializer.Meta.fields + ('relation',)

    def get_relation(self, instance):
        main_user = self.context['main_user']
        if not isinstance(main_user, AnonymousUser):
            return friend_request_status(main_user, get_friends(instance), get_subscriptions(instance),
                                         get_requested(instance))
        return None
