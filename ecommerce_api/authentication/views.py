from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from authentication.serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer


class ObtainAuthTokenView(ObtainAuthToken, generics.GenericAPIView):
    """
    Return token from user
    """
    permission_classes = [permissions.IsAdminUser]


class NewAuthTokenView(ObtainAuthToken, generics.GenericAPIView):
    """
    Return a new token from user
    """

    permission_classes = [permissions.IsAdminUser]
    
    def post(self, request, *args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            if not created:
                key = token.generate_key()
                Token.objects.filter(user=user).update(key=key)

            return Response({'token': key}, 200)
        except Exception as e:
            print(str(e))
            return Response({'error': str(e)}, 400)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    https://django-rest-framework-simplejwt.readthedocs.io
    """
    serializer_class = CustomTokenObtainPairSerializer
    
    def delete(self, *args, **kwargs):
        return Response(status=200)


class CustomTokenRefreshView(TokenRefreshView):

    serializer_class = CustomTokenRefreshSerializer
