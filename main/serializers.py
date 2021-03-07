from rest_framework import serializers
from user.models import NewUser
from main.models import Messages, Friends


class CurrentFriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = (
            'id', 'username',
        )


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = (
            'who', 'whom', 'message'
        )

    def create(self, validated_data):
        cr_message = Messages(
            who=validated_data['who'],
            whom=validated_data['whom'],
            message=validated_data['message']
        )
        new_message = Messages.objects.create(who=validated_data['who'], whom=validated_data['whom'],
                                              message=validated_data['message'])
        return new_message


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = (
            'who', 'whom',
        )

    def create(self, validated_data):
        likes = Friends(who=validated_data['who'], whom=validated_data['whom'])
        likes.save()
        return likes
