from rest_framework.routers import DefaultRouter
from deals import views

app_name='deals'
router = DefaultRouter()
router.register(r'', views.DealsView, basename='deals')

urlpatterns = router.urls