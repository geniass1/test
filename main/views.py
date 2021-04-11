from user.models import NewUser
from main.models import Friends, Messages
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from main.serializers import CurrentFriendsSerializer, MessageSerializer, ReactionSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from user_profile.services import get_friends, get_requested, get_subscriptions


class ManageSubscriptions(APIView):
    def delete(self, request):
        user = request.user
        friend = get_object_or_404(Friends, who=user.id, whom=request.data['id'])
        friend.delete()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)


class Reaction(APIView):
    def post(self, request):
        user = request.user
        if 'isRejectRequest' in request.data:
            friend = Friends.objects.get(who=request.data['id'], whom=user.id)
            friend.pending = False
            friend.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        if Friends.objects.filter(who=user.id, whom=request.data['id']).count() > 0:
            return Response('Relation already exists', status=status.HTTP_409_CONFLICT)
        serializer = ReactionSerializer(data={'who': user.id, 'whom': request.data['id']})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        friend = get_object_or_404(Friends, who=user.id, whom=request.data['id'])
        reversed_friend = get_object_or_404(Friends, whom=user.id, who=request.data['id'])
        reversed_friend.pending = False
        friend.delete()
        reversed_friend.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)


class Message(APIView):
    def get(self, request):
        user = request.user
        if 'id' in request.GET:
            all_messages = Messages.objects.all().filter(
                Q(who=user, whom__id=request.GET['id']) | Q(who__id=request.GET['id'], whom=user))
            all_messages = [MessageSerializer(instance=message).data for message in all_messages]
            return Response({'all_messages': all_messages}, status=status.HTTP_200_OK)
        else:
            messages = Messages.objects.raw(
                '''
                SELECT *
                FROM main_messages AS main
                WHERE 
                    (
                        main.id = (
                            SELECT max(id) 
                            FROM (
                                SELECT id 
                                FROM main_messages
                                WHERE
                                    (who_id = :user_id) and
                                    ((whom_id = main.whom_id) or (whom_id = main.who_id)) and 
                                    (whom_id != :user_id)
                                UNION ALL 
                                SELECT id 
                                FROM main_messages
                                WHERE 
                                    (whom_id = :user_id) and
                                    ((who_id = main.whom_id) or (who_id = main.who_id)) and
                                    (who_id != :user_id)
                        )
                    ) OR (
                        main.id = (
                            SELECT max(id)
                            FROM main_messages
                            WHERE 
                                (whom_id = :user_id) and
                                (who_id = :user_id)
                        )
                    ) 
                )
                ORDER BY id DESC                   
                ''',
                {"user_id": user.id}
            )
            all_messages = [MessageSerializer(instance=message).data for message in messages]
            return Response({'all_messages': all_messages}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MessageSerializer(
            data={'who': request.user.id, 'whom': request.data['id'], 'message': request.data['message']})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentFriends(APIView):
    def get(self, request, id):
        user = NewUser.objects.get(id=id)
        friends = get_friends(user)
        serializer = [CurrentFriendsSerializer(instance=post, context={'request': request}).data for post in friends]
        return Response({'friends': serializer}, status=status.HTTP_200_OK)


class Subscriptions(APIView):
    def get(self, request, id):
        user = NewUser.objects.get(id=id)
        subscriptions = get_subscriptions(user)
        serializers = CurrentFriendsSerializer(subscriptions, context={'request': request}, many=True)
        return Response({'subscriptions': serializers.data}, status=status.HTTP_200_OK)


class Requested(APIView):
    def get(self, request, id):
        user = NewUser.objects.get(id=id)
        requested = get_requested(user)
        serializers = CurrentFriendsSerializer(requested, context={'request': request}, many=True)
        return Response({'requests': serializers.data}, status=status.HTTP_200_OK)
