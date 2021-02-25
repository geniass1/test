from user.models import NewUser
import jwt


from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializers import UserSerializer, ChangeSerializer


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"ERROR": serializer.errors})


class ChangeInfo(APIView):
    def post(self, request):
        user = NewUser.objects.get(username=request.data['username'])
        serializer = ChangeSerializer(data=request.data, instance=user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class Login(APIView):
    def post(self, request):
        if NewUser.objects.get(username=request.data['username']).check_password(request.data['password']):
            key = 'secret'
            encoded = jwt.encode({'username': request.data['username']}, key, algorithm='HS256')
            return Response({"token": encoded})
