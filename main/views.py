from user.models import NewUser
from main.models import Friends, Messages
from user_profile.models import UserProfile
from django.db.models import Q
from django.db.models import Exists, OuterRef
import jwt

from rest_framework.response import Response
from rest_framework.views import APIView
from main.serializers import CurrentFriendsSerializer, MessageSerializer, ReactionSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


class Reaction(APIView):
    def post(self, request):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
        user = NewUser.objects.get(username=username['username'])
        data = dict(request.data.items())
        data['who'] = user.id
        data['whom'] = data['id']
        serializer = ReactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
        user = NewUser.objects.get(username=username['username'])
        friend = get_object_or_404(Friends, who=user.id, whom=id)
        friend.delete()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)


class Message(APIView):
    def get(self, request, id):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
        user = NewUser.objects.get(username=username['username'])
        all_messages = Messages.objects.all().filter(
            Q(who=user, whom__id=id) | Q(who__id=id, whom=user))
        all_messages = [MessageSerializer(instance=message).data for message in all_messages]
        return Response({'all_messages': all_messages}, status=status.HTTP_200_OK)

    def post(self, request, id):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
        data = dict(request.data.items())
        data['who'] = NewUser.objects.get(username=username['username']).id
        data['whom'] = id
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentFriends(APIView):
    def get(self, request, id):
        # username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
        # user = NewUser.objects.get(username=username['username'])
        user = NewUser.objects.get(id=id)
        qs = NewUser.objects.filter(
            Exists(Friends.objects.filter(who=user, whom__id=OuterRef('pk')))).filter(
            Exists(Friends.objects.filter(who__id=OuterRef('pk'), whom=user))
        ).distinct()
        serializer = [CurrentFriendsSerializer(instance=post).data for post in qs]
        for friend in serializer:
            try:
                friend['image'] = request.build_absolute_uri((UserProfile.objects.get(id=friend['id'])).image.image.url)
            except:
                friend['image'] = None
        return Response(serializer, status=status.HTTP_200_OK)


class Subscriptions(APIView):
    def get(self, request, id):
        # username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
        # user = NewUser.objects.get(username=username['username'])
        user = NewUser.objects.get(id=id)
        qs = NewUser.objects.filter(
            ~Exists(Friends.objects.filter(who=user, whom__id=OuterRef('pk')))).filter(
            Exists(Friends.objects.filter(who__id=OuterRef('pk'), whom=user))
        ).distinct()
        serializers = CurrentFriendsSerializer(qs, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)