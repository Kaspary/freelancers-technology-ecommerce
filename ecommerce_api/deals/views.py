from deals.models import Bid, Deal, Message
from deals.serializer import BidSerializer, DealSerializer, MessageSerializer
from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions, viewsets

from correios.dtos import CorreiosRequest
from correios.integracao import calc_price_and_deadline

calc_price_and_deadline(
        CorreiosRequest(
            nCdEmpresa='09146920',
            sDsSenha=123456,
            sCepOrigem=70002900,
            sCepDestino=71939360,
            nVlPeso=1,
            nCdFormato=1,
            nVlComprimento=30,
            nVlAltura=30,
            nVlLargura=30,
            sCdMaoPropria='n',
            nVlValorDeclarado=0,
            sCdAvisoRecebimento='n',
            nCdServico=40010,
            nVlDiametro=0,
            StrRetorno='xml',
            nIndicaCalculo=3
        )
    )

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
