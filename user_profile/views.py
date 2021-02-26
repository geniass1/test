from user.models import NewUser
from user_profile.models import UserPosts, UserProfile
from django.db.models import Q
from django.db.models import Exists, OuterRef
import jwt

from rest_framework.response import Response
from rest_framework.views import APIView
from user_profile.serializers import UserPostSerializer


class UserPost(APIView):
    def get(self, request, id):
        username = NewUser.objects.get(id=id)
        all_posts = UserPosts.objects.all().filter(user=username.id)
        all_posts = [UserPostSerializer(instance=post).data for post in all_posts]
        return Response({'all_posts': all_posts})

    def post(self, request):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
        data = dict(request.data.items())
        data['user'] = NewUser.objects.get(username=username['username']).id
        serializer = UserPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

