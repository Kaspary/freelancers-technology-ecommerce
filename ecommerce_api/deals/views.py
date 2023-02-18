from deals.filters import DeliveryFilter
from deals.models import Bid, Deal, Message
from deals.serializer import (BidSerializer, DealSerializer,
                              DeliverySerializer, MessageSerializer)
from django.contrib.auth.models import AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.response import Response

from delivery.actions import calc_delivery_between_ceps


class DealsView(viewsets.ModelViewSet):
    """
    Manager Deals
    """

    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Deal.objects.all()

    serializer_class = DealSerializer

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser) or not self.request.user.is_manager:
            queryset = self.queryset.filter(user__id=self.request.user.id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context


class BidView(viewsets.ModelViewSet):
    """
    Manager Deals
    """

    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Bid.objects.all()

    serializer_class = BidSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(deal__id=self.kwargs.get("deal_id"))
        if isinstance(self.request.user, AnonymousUser) or not self.request.user.is_manager:
            queryset = self.queryset.filter(user__id=self.request.user.id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["deal_id"] = self.kwargs.get("deal_id")
        context["user"] = self.request.user
        return context


class MessageView(viewsets.ModelViewSet):
    """
    Manager Deals
    """

    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Message.objects.all()

    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(deal__id=self.kwargs.get("deal_id"))
        if isinstance(self.request.user, AnonymousUser) or not self.request.user.is_manager:
            queryset = self.queryset.filter(user__id=self.request.user.id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["deal_id"] = self.kwargs.get("deal_id")
        context["user"] = self.request.user
        return context


class DeliveryView(mixins.RetrieveModelMixin, generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeliverySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeliveryFilter

    def get(self, request, deal_id=None, *args, **kwargs):
        deal = Deal.objects.get(id=deal_id)
        delivery = calc_delivery_between_ceps(
            cep_origin=deal.location.zip_code,
            cep_destination=request.user.location.zip_code,
            value=0,
            weight=30,
            length=30,
            height=30,
            width=1,
            diameter=0
        )
        delivery_map = {
            "code": delivery.Codigo,
            "value": delivery.Valor,
            "own_hand_value": delivery.ValorMaoPropria,
            "value_notice_receipt": delivery.ValorAvisoRecebimento,
            "declared_value": delivery.ValorValorDeclarado,
            "deadline": delivery.PrazoEntrega,
            "value_without_additionals": delivery.ValorSemAdicionais,
            "home_delivery": delivery.home_delivery,
            "delivery_in_saturday": delivery.delivery_in_saturday
        }
        return Response(self.get_serializer_class()(delivery_map).data, status=200)
