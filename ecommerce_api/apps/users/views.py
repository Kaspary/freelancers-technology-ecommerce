from django.conf import settings
from apps.users.models import ConfirmEmailToken
from apps.users.serializers import (
    CustomTokenObtainPairSerializer,
    UpdateUserSerializer,
    UserSerializer
)
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from ecommerce_api.apps.users.permissions import IsSelfOrAdmin


class UserView(viewsets.ModelViewSet):
    """
    manager users
    """
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    # Change the serializer class by method
    def get_serializer_class(self):
        if self.request.method in ['PUT',]:
            return UpdateUserSerializer
        return self.serializer_class

    # return correct permission to method
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action == 'list':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        elif self.action in ('retrieve', 'update', 'destroy'):
            return [permissions.IsAuthenticated(), IsSelfOrAdmin()]
