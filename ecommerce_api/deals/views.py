from deals.models import Bid, Deal
from rest_framework import viewsets

from deals.serializer import BidSerializer, DealResultSerializer, DealSerializer


class DealsView(viewsets.ModelViewSet):
    """
    Manager Deals
    """
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = Deal.objects.all()

    serializer_class = None
    
    read_serializer_class = DealResultSerializer
    write_serializer_class = DealSerializer

    def get_serializer_class(self):    
        # if self.action in ("retrieve", "list"):
        #     return self.read_serializer_class
        return self.write_serializer_class

    def get_queryset(self):
        queryset = Deal.objects.filter(user__id=self.request.user.id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user
        return context
    

    # def retrieve(self, request, *args, **kwargs):
    #     # self.queryset = self.get_queryset().filter(user = request.user.id)
    #     result = super().list(request, *args, **kwargs)
    #     return result

    # def list(self, request, *args, **kwargs):
    #     # self.queryset = self.get_queryset().filter(user=request.user.id)
    #     result = super().list(request, *args, **kwargs)
    #     return result


class BidView(viewsets.ModelViewSet):
    """
    Manager Deals
    """
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = Bid.objects.all()

    serializer_class = BidSerializer

    def get_queryset(self):
        deal_id = self.kwargs.get('deal_id')
        queryset = Bid.objects.filter(deal__id=deal_id, user__id=self.request.user.id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['deal_id'] = self.kwargs.get('deal_id')
        context['user_id'] = self.request.user
        return context
