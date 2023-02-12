from django.urls import path
from apps.authentication import views


urlpatterns = [
    path('', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
]