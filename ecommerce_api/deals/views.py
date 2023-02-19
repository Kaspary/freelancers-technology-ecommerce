from deals.filters import DeliveryFilter
from deals.models import Bid, Deal, Message, Payment
from deals.serializer import (
    BidSerializer,
    DealSerializer,
    DeliverySerializer,
    MessageSerializer,
    PaymentSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.response import Response

from delivery.actions import calc_delivery_between_ceps
from common.views import BaseGenericAPIView, BaseModelViewSet


class DealsView(BaseModelViewSet):
    """
    Manager Deals
    """
    queryset = Deal.objects.all()
    serializer_class = DealSerializer


class BaseDealView(BaseModelViewSet):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(deal__id=self.kwargs.get("deal_id"))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["deal_id"] = self.kwargs.get("deal_id")
        return context


class BidView(BaseDealView):
    """
    Manager Bid
    """

    queryset = Bid.objects.all()
    serializer_class = BidSerializer


class MessageView(BaseDealView):
    """
    Manager message
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer



class DeliveryView(mixins.RetrieveModelMixin, BaseGenericAPIView):
    serializer_class = DeliverySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeliveryFilter

    def get(self, request, deal_id=None, *args, **kwargs):

        if not request.user.location:
            return Response({'message': "User doesn't have an address"}, status=400)

        deal = Deal.objects.get(id=deal_id)
        delivery = calc_delivery_between_ceps(
            cep_origin=deal.location.zip_code,
            cep_destination=request.user.location.zip_code,
            value=deal.value,
            weight=deal.product.weight,
            length=deal.product.length,
            height=deal.product.height,
            width=deal.product.width,
            diameter=deal.product.diameter
        )

        if delivery.MsgErro: 
            return Response({'message': delivery.MsgErro}, status=400)

        delivery_map = {
            "code": delivery.Codigo,
            "value": delivery.Valor,
            "own_hand_value": delivery.ValorMaoPropria,
            "value_notice_receipt": delivery.ValorAvisoRecebimento,
            "declared_value": delivery.ValorValorDeclarado,
            "deadline": delivery.PrazoEntrega,
            "value_without_additionals": delivery.ValorSemAdicionais,
            "home_delivery": delivery.home_delivery,
            "delivery_in_saturday": delivery.delivery_in_saturday,
        }
        return Response(self.get_serializer(delivery_map).data, status=200)


class PaymentView(
    mixins.RetrieveModelMixin, mixins.CreateModelMixin, BaseGenericAPIView):
    
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get(self, request, deal_id=None, *args, **kwargs):
        try:
            payment = self.get_queryset().get(id=deal_id)
            return Response(self.get_serializer(payment).data, status=200)
        except Payment.DoesNotExist: 
            return Response(status=200)

    
    def post(self, request, deal_id=None, *args, **kwargs):
        
        """Implement here the rules of payment"""

        payment_serializer = PaymentSerializer(data={'deal': deal_id, 'user': request.user.id})
        payment_serializer.is_valid(raise_exception=True)
        payment_serializer.save()

        return Response(payment_serializer.data, status=200)
