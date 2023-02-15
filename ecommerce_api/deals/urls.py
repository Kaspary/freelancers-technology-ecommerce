from os import path
from rest_framework.routers import DefaultRouter
from deals import views

app_name='deals'
router = DefaultRouter()
router.register(r'(?P<deal_id>\d+)/bids', views.BidView, basename='bids')
router.register(r'', views.DealsView, basename='deals')

urlpatterns = router.urls
