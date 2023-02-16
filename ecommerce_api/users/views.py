from users.serializers import InviteSerializer, UserSerializer
from users.models import Invite, User
from rest_framework import permissions, viewsets

from users.permissions import IsSelfOrAdmin


class UserView(viewsets.ModelViewSet):
    """
    manage users
    """
    http_method_names = ['get', 'post', 'put', 'delete']
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



class InviteView(viewsets.ModelViewSet):
    """
    manage invites
    """
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = Invite.objects.all().order_by('created_at')
    serializer_class = InviteSerializer
    
    def get_permissions(self):
        if self.action in ('update', 'destroy'):
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = self.queryset.filter(user__id=self.request.user.id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context