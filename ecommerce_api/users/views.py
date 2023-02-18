from common.views import BaseModelViewSet
from users.serializers import InviteSerializer, UserSerializer
from users.models import Invite, User
from rest_framework import permissions, viewsets

from users.permissions import IsSelfOrAdmin


class UserView(BaseModelViewSet):
    """
    Manage users
    """
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer

    # return correct permission to method
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action == 'list':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        elif self.action in ('retrieve', 'update', 'destroy'):
            return [permissions.IsAuthenticated(), IsSelfOrAdmin()]
        
        return super().get_permissions()



class InviteView(BaseModelViewSet):
    """
    Manage invites
    """
    queryset = Invite.objects.all().order_by('created_at')
    serializer_class = InviteSerializer
    
    def get_permissions(self):
        if self.action in ('update', 'destroy'):
            return [permissions.IsAdminUser()]
        
        return super().get_permissions()