from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer
)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, *args, **kwargs):
        tokens = super().validate(*args, **kwargs)
        return {
            'token':{
                'access_token': tokens.pop('access'),
                'refresh_token': tokens.pop('refresh')
            }
        }
        
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        # ...

        return token


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    
    def validate(self, *args, **kwargs):
        tokens = super().validate(*args, **kwargs)
        return {
            'token':{
                'access_token': tokens.pop('access'),
                'refresh_token': tokens.pop('refresh')
            }
        }
