from rest_framework.routers import DefaultRouter
from users import views

app_name='users'
router = DefaultRouter()
router.register(r'invites', views.InviteView, basename='invite')
router.register(r'', views.UserView, basename='user')

urlpatterns = router.urls