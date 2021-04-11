from rest_framework import serializers
from user.models import NewUser
from main.models import Messages, Friends


class CurrentFriendsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = NewUser
        fields = (
            'id', 'username', 'image'
        )

    def get_image(self, user):
        request = self.context['request']
        image = user.user_profile.image
        if image is None:
            return None
        return request.build_absolute_uri(image.image.url)


class MessageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Messages
        fields = (
            'who', 'whom', 'message', 'image', 'username'
        )

    def create(self, validated_data):
        new_message = Messages.objects.create(who=validated_data['who'], whom=validated_data['whom'],
                                              message=validated_data['message'])
        return new_message

    def get_image(self, user):
        request = self.context['request']
        image = user.whom.user_profile.image
        if image is None:
            return None
        return request.build_absolute_uri(image.image.url)

    def get_username(self, user):
        return user.whom.username


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = (
            'who', 'whom',
        )

    def create(self, validated_data):
        likes = Friends(who=validated_data['who'], whom=validated_data['whom'], pending=True)
        likes.save()
        return likes
