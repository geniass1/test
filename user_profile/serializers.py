from rest_framework import serializers
from .models import UserPosts, UserProfile
from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from django.core.files.base import ContentFile
import base64
import six
import uuid
import imghdr

class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
            	# Break out the header from the base64 content
            	header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
            	decoded_file = base64.b64decode(data)
            except TypeError:
            	self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):

    	extension = imghdr.what(file_name, decoded_file)
    	extension = "jpg" if extension == "jpeg" else extension

    	return extension



class UserPostSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None, use_url=True,
    )
    class Meta:
        model = UserPosts
        fields = (
            'image', 'title', 'id', 'user',
        )

    def create(self, validated_data):
        breakpoint()
        try:
            image_data = validated_data.pop('image')
        except:
            image_data = None
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



