from user.models import NewUser
from user_profile.models import UserPosts, Likes, UserProfile
import jwt

from rest_framework.response import Response
from rest_framework.views import APIView
from user_profile.serializers import UserPostSerializer, UserProfileSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


class UserPostGet(APIView):
    def get(self, request, id):
        username = get_object_or_404(NewUser, id=id)
        all_posts = UserPosts.objects.all().filter(user=username.id)
        all_posts = [UserPostSerializer(instance=post).data for post in all_posts]
        return Response({'all_posts': all_posts}, status=status.HTTP_200_OK)


class UserPost(APIView):
    def post(self, request):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
        data = dict(request.data.items())
        data['user'] = NewUser.objects.get(username=username['username']).id
        serializer = UserPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = dict(serializer.data.items())
            if 'image' in data and data['image'] != None:
                data['image'] = request.build_absolute_uri(data['image'])
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPostLikes(APIView):
    def post(self, request, id):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1],
                              'secret', algorithms=['HS256'])
        user = NewUser.objects.get(username=username['username'])
        post = get_object_or_404(UserPosts, id=id)
        like, _ = Likes.objects.get_or_create(user_id=user.id, post_id=post.id)
        if like.is_liked:
            like.is_liked = False
            post.likes -= 1
            like.save()
            post.save()
            return Response({'status': 'like was deleted'}, status=status.HTTP_200_OK)
        else:
            like.is_liked = True
            post.likes += 1
            like.save()
            post.save()
            return Response({'status': 'like was added'}, status=status.HTTP_200_OK)


class UserProfilePost(APIView):
    def post(self, request):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
        data = dict(request.data.items())
        data['user'] = NewUser.objects.get(username=username['username']).id
        if 'image' in request.data and 'image' != None:
            serializer = UserPostSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                data['image'] = serializer.data['id']
        instance = UserProfile.objects.get(id=data['user'])
        serializer = UserProfileSerializer(data=data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileGet(APIView):
    def get(self, request, id):
        if id == 0:
            username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
            data = dict(request.data.items())
            data['user'] = NewUser.objects.get(username=username['username']).id
            id = data['user']
        user_profile = UserProfile.objects.get(user=id)
        user_profile = UserProfileSerializer(user_profile)
        data = dict(user_profile.data.items())
        if 'image' in data and data['image'] != None:
            data['image'] = request.build_absolute_uri(UserPosts.objects.get(id=data['image']).image.url)
        data['username'] = NewUser.objects.get(id=id).username
        return Response({'user': data}, status=status.HTTP_200_OK)







