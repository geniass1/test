from user.models import NewUser
from user_profile.models import UserPosts, Likes, UserProfile, Comments
from rest_framework.response import Response
from rest_framework.views import APIView
from user_profile.serializers import UserPostSerializer, UserProfileSerializer, UserProfileMySerializer, \
    UserProfileReadSerializer
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from user_profile.services import get_friends, get_subscriptions, get_requested


class UserPost(APIView):
    def get(self, request, id):
        username = get_object_or_404(NewUser, id=id)
        all_posts = UserPosts.objects.all().filter(user=username.id)
        all_posts = [UserPostSerializer(instance=post).data for post in all_posts]
        for post in all_posts:
            if post['image'] is not None:
                post['image'] = request.build_absolute_uri(post['image'])
                post['comments'] = Comments.objects.get(post=post['id'])
        return Response({'all_posts': all_posts}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        permission_classes = (permissions.IsAuthenticated,)
        if UserPosts.objects.get(id=id).user.id == request.user.id:
            post = UserPosts.objects.get(id=id)
            post.delete()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        return Response({'status': 'error'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        permission_classes = (permissions.IsAuthenticated,)
        data = dict(request.data.items())
        data['user'] = request.user.id
        serializer = UserPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = dict(serializer.data.items())
            if 'image' in data and data['image'] is not None:
                data['image'] = request.build_absolute_uri(data['image'])
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPostLikes(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        post = get_object_or_404(UserPosts, id=id)
        like, _ = Likes.objects.get_or_create(user_id=request.user.id, post_id=post.id)
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
            return Response({'status': 'like was created'}, status=status.HTTP_200_OK)


class UserPostComments(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        post = get_object_or_404(UserPosts, id=id)
        comment = Comments.objects.create(user=request.user, post=post, comment=request.data['comment'])
        return Response({'status': 'success'}, status=status.HTTP_200_OK)


class UserProfilePost(APIView):
    def post(self, request):
        data = dict(request.data.items())
        data['user'] = request.user.id
        if 'image' in request.data and 'image' is not None:
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


class UserProfileMyGet(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        user.profile = get_object_or_404(UserProfile, user=user)
        friends = get_friends(user)
        user.friends = friends[:5]
        user.friends_count = friends.count()
        user.subscriptions = get_subscriptions(user)
        user.requested = get_requested(user)
        return Response(
            UserProfileMySerializer(instance=user, context={'request': request}).data, status=status.HTTP_200_OK
        )


class UserProfileGet(APIView):
    def get(self, request, id):
        user = get_object_or_404(NewUser, id=id)
        user.profile = get_object_or_404(UserProfile, user=user)
        friends = get_friends(user)
        user.friends = friends[:5]
        user.friends_count = friends.count()
        user.subscriptions = get_subscriptions(user)
        user.requested = get_requested(user)

        return Response(
            UserProfileReadSerializer(instance=user,
                                      context={'request': request, 'main_user': request.user}).data,
            status=status.HTTP_200_OK
        )
