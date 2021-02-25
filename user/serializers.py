from rest_framework import serializers
from user.models import NewUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = (
            'username', 'email', 'password', 'id',
        )

    def create(self, validated_data):
        user = NewUser(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangeSerializer(serializers.Serializer):
    new_username = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    new_password = serializers.CharField()

    def update(self, instance, validated_data):
        instance.username = validated_data['new_username']
        if instance.check_password(validated_data['password']):
            instance.set_password(validated_data['new_password'])
            instance.save()
            return instance

    def to_representation(self, instance):
        return {}



