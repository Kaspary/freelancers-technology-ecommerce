from rest_framework.routers import DefaultRouter
from apps.users import views

app_name='users'
router = DefaultRouter()
router.register(r'', views.UserView, basename='user')

urlpatterns = router.urls