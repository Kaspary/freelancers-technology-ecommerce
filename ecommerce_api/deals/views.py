from deals.models import Bid, Deal
from rest_framework import viewsets, permissions

from deals.serializer import BidSerializer, DealResultSerializer, DealSerializer


class DealsView(viewsets.ModelViewSet):
    """
    Manager Deals
    """

    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Deal.objects.all()

    serializer_class = DealSerializer

    def get_queryset(self):
        if not self.request.user.is_manager:
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
        if not self.request.user.is_manager:
            queryset = self.queryset.filter(user__id=self.request.user.id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["deal_id"] = self.kwargs.get("deal_id")
        context["user"] = self.request.user
        return context
