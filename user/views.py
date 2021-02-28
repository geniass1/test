from user.models import NewUser
import jwt

from user_profile.models import UserProfile
from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializers import UserSerializer, ChangeSerializer
from rest_framework import status


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserProfile.objects.create(user=NewUser.objects.get(id=serializer.data['id']))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ChangeInfo(APIView):
    def post(self, request):
        user = NewUser.objects.get(username=request.data['username'])
        serializer = ChangeSerializer(data=request.data, instance=user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        try:
            if NewUser.objects.get(username=request.data['username']).check_password(request.data['password']):
                key = 'secret'
                encoded = jwt.encode({'username': request.data['username']}, key, algorithm='HS256')
                return Response({'token': encoded}, status=status.HTTP_200_OK)
            raise NewUser.DoesNotExist
        except NewUser.DoesNotExist:
            return Response({'status': 'failed',
                         'error': {'credentials': ['wrong password or login']}}, status=status.HTTP_400_BAD_REQUEST)
