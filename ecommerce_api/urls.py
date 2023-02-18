from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, re_path
from django.conf.urls.static import static
from swagger import urlpatterns as swagger_urlpatterns


urlpatterns = [
    # System urls
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^accounts/', include('rest_framework.urls')),
    
    # Docs
    *swagger_urlpatterns,

    # Application
    re_path(r'^api/(?P<version>(v1|v2))/users/', include('users.urls'), name='Users'),
    re_path(r'^api/(?P<version>(v1|v2))/authenticate/', include('authentication.urls'), name='Authenticate'),
    re_path(r'^api/(?P<version>(v1|v2))/deals/', include('deals.urls'), name='Deals'),

    # Statics
    *staticfiles_urlpatterns(),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]