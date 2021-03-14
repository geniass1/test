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
        if 'accept' in request.data:
            friend = Friends.objects.get(whom=user.id, who=data['id'])
            friend.pending = False
            friend.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        try:
            friend = Friends.obejects.get(whom=user.id, who=data['id'])
            friend.pending = False
            friend.save()
        except:
            pass
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
    def get(self, request):
        if request.GET['id'] == '0':
            username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
            id = NewUser.objects.get(username=username['username']).id
        else:
            id = request.GET['id']
        user = NewUser.objects.get(id=id)
        friends = NewUser.objects.filter(
            Exists(Friends.objects.filter(who=user, whom__id=OuterRef('pk')))).filter(
            Exists(Friends.objects.filter(who__id=OuterRef('pk'), whom=user))
        ).distinct()
        serializer = [CurrentFriendsSerializer(instance=post).data for post in friends]
        for friend in serializer:
            # breakpoint()
            try:
                friend['image'] = request.build_absolute_uri((UserProfile.objects.get(id=friend['id'])).image.image.url)
            except:
                friend['image'] = None
            if "Authorization" in request.headers:
                username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
                id = NewUser.objects.get(username=username['username']).id
                if Friends.objects.filter(who=id, whom=friend['id']).count()>0:
                    friend['isFriend'] = True
                else:
                    friend['isFriend'] = False
        return Response({'friends': serializer}, status=status.HTTP_200_OK)


class Subscriptions(APIView):
    def get(self, request):
        if request.GET['id'] == '0':
            username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
            id = NewUser.objects.get(username=username['username']).id
        else:
            id = request.GET['id']
        user = NewUser.objects.get(id=id)
        qs = NewUser.objects.filter(
            ~Exists(Friends.objects.filter(who=user, whom__id=OuterRef('pk')))).filter(
            Exists(Friends.objects.filter(who__id=OuterRef('pk'), whom=user))
        ).distinct()

        serializers = CurrentFriendsSerializer(qs, many=True)
        return Response({'subscriptions': serializers.data}, status=status.HTTP_200_OK)


class Requested(APIView):
    def get(self, request):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], 'secret', algorithms=['HS256'])
        user = NewUser.objects.get(username=username['username']).id
        requested = NewUser.objects.filter(
            ~Exists(Friends.objects.filter(who=user, whom__id=OuterRef('pk')))).filter(
            Exists(Friends.objects.filter(who__id=OuterRef('pk'), whom=user, pending=True))
        ).distinct()

        serializers = CurrentFriendsSerializer(requested, many=True)
        return Response({'requests': serializers.data}, status=status.HTTP_200_OK)