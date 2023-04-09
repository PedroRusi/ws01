from django.contrib.auth import logout
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import BearerAuthentication
from .models import User
from .serializers import LoginSerializer, RegistrSerializer


# Create your views here.
class LoginAPIView(APIView):
    permission_classes = ()
    authentication_classes = (BearerAuthentication, )

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'data': {
                 'user_token': token.key
               }
            }, status=status.HTTP_200_OK)
        return Response({
                   'error': {
                     'code': 401,
                     'message': 'Authentication failed'
                   }
                },
            status=status.HTTP_401_UNAUTHORIZED)


class RegistrAPIView(APIView):
    permission_classes = ()
    authentication_classes = (BearerAuthentication, )

    def post(self, request):
        serializer = RegistrSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogOut(APIView):

    def post(self, request=WSGIRequest):
        try:
            request.user.auth_token.delete()
        except:
            return Response({"error": "Logout failed"}, status=status.HTTP_401_UNAUTHORIZED)

        logout(request)

        return Response()