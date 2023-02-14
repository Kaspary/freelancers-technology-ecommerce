from deals.models import Deals
from rest_framework import viewsets

from deals.serializer import NegotiatonResultSerializer, NegotiatonSerializer


class DealsView(viewsets.ModelViewSet):
    """
    Manager Deals
    """
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = Deals.objects.all()

    serializer_class = None
    
    read_serializer_class = NegotiatonResultSerializer
    write_serializer_class = NegotiatonSerializer

    def get_serializer_class(self):    
        # if self.action in ("retrieve", "list"):
        #     return self.read_serializer_class
        return self.write_serializer_class
    

    # def retrieve(self, request, *args, **kwargs):
    #     # self.queryset = self.get_queryset().filter(user = request.user.id)
    #     result = super().list(request, *args, **kwargs)
    #     return result

    # def list(self, request, *args, **kwargs):
    #     # self.queryset = self.get_queryset().filter(user=request.user.id)
    #     result = super().list(request, *args, **kwargs)
    #     return result