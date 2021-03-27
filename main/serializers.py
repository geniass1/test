import jwt
from rest_framework import serializers
from user.models import NewUser
from main.models import Messages, Friends


class CurrentFriendsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    isFriend = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = NewUser
        fields = (
            'id', 'username', 'image', 'isFriend'
        )

    def get_image(self, user):
        request = self.context['request']
        image = user.user_profile.image
        if image is None:
            return None
        return request.build_absolute_uri(image.image.url)

    def get_isFriend(self, user):
        request = self.context['request']
        if "Authorization" in request.headers:
            username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
            id = NewUser.objects.get(username=username['username']).id
            if Friends.objects.filter(who=id, whom=user.id).count() > 0:
                return True
            return False
        return False


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
        likes = Friends(who=validated_data['who'], whom=validated_data['whom'], pending=True)
        likes.save()
        return likes
