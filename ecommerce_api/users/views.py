from users.serializers import UserSerializer
from users.models import User
from rest_framework import permissions, viewsets

from users.permissions import IsSelfOrAdmin


class UserView(viewsets.ModelViewSet):
    """
    manager users
    """
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    # return correct permission to method
    def get_permissions(self):
        return [permissions.AllowAny()]
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action == 'list':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        elif self.action in ('retrieve', 'update', 'destroy'):
            return [permissions.IsAuthenticated(), IsSelfOrAdmin()]
