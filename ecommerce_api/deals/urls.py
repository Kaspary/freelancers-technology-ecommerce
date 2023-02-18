from django.urls import re_path
from rest_framework.routers import DefaultRouter
from deals import views

app_name='deals'
router = DefaultRouter()
router.register(r'(?P<deal_id>\d+)/messages', views.MessageView, basename='messages')
router.register(r'(?P<deal_id>\d+)/bids', views.BidView, basename='bids')
router.register(r'', views.DealsView, basename='deals')

urlpatterns = [
    re_path('(?P<deal_id>\d+)/deliveries', views.DeliveryView.as_view(), name='delivery'),
] + router.urls
