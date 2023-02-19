from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import FieldError
class BaseModelViewSet(ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        queryset = super().get_queryset()
        is_anonymous = isinstance(self.request.user, AnonymousUser)
        if is_anonymous or not self.request.user.is_manager:
            try:
                queryset = queryset.filter(user__id=self.request.user.id)
            except FieldError:
                pass
        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context


class BaseGenericAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        queryset = super().get_queryset()
        is_anonymous = isinstance(self.request.user, AnonymousUser)
        if is_anonymous or not self.request.user.is_manager:
            queryset = queryset.filter(user__id=self.request.user.id)
        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context