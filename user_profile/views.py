from user.models import NewUser
from user_profile.models import UserPosts, UserProfile, Likes
from django.db.models import Q
from django.db.models import Exists, OuterRef
import jwt

from rest_framework.response import Response
from rest_framework.views import APIView
from user_profile.serializers import UserPostSerializer


class UserPostGet(APIView):
    def get(self, request, id):
        username = NewUser.objects.get(id=id)
        all_posts = UserPosts.objects.all().filter(user=username.id)
        all_posts = [UserPostSerializer(instance=post).data for post in all_posts]
        return Response({'all_posts': all_posts})


class UserPost(APIView):
    def post(self, request):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
        data = dict(request.data.items())
        data['user'] = NewUser.objects.get(username=username['username']).id
        serializer = UserPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class UserPostLikes(APIView):
    def post(self, request, id):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
        data = dict(request.data.items())
        data['user'] = NewUser.objects.get(username=username['username']).id
        post = UserPosts.objects.get(id=id)
        try:
            like = Likes.objects.get(user=data['user'], post=post.id)
            if like.is_liked:
                like.is_liked = False
                post.likes -= 1
            return Response({'Warning': 'like was deleted'})
        except:
            like = Likes.objects.create(user=data['user'], post=post.id, is_liked=True)
            post.likes += 1
            return Response({'Warning': 'like was created'})





