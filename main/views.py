from user.models import NewUser
from main.models import Friends, Messages
from django.db.models import Q
from django.db.models import Exists, OuterRef
import jwt

from rest_framework.response import Response
from rest_framework.views import APIView
from main.serializers import CurrentFriendsSerializer, MessageSerializer, ReactionSerializer


class Reaction(APIView):
    def post(self, request, id):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
        user = NewUser.objects.get(username=username['username'])
        data = dict(request.data.items())
        data['who'] = user.id
        data['whom'] = id
        serializer = ReactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class Message(APIView):
    def get(self, request, id):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
        user = NewUser.objects.get(username=username['username'])
        all_messages = Messages.objects.all().filter(
            Q(who=user, whom__id=id) | Q(who__id=id, whom=user))
        all_messages = [MessageSerializer(instance=message).data for message in all_messages]
        return Response({'all_messages': all_messages})

    def post(self, request, id):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
        data = dict(request.data.items())
        data['who'] = NewUser.objects.get(username=username['username']).id
        data['whom'] = id
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CurrentFriends(APIView):
    def get(self, request):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
        user = NewUser.objects.get(username=username['username'])
        qs = NewUser.objects.filter(
            Exists(Friends.objects.filter(who=user, whom__id=OuterRef('pk')))).filter(
            Exists(Friends.objects.filter(who__id=OuterRef('pk'), whom=user))
        ).distinct()
        serializers = CurrentFriendsSerializer(qs, many=True)
        return Response(serializers.data)
