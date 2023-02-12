from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_yasg.generators import OpenAPISchemaGenerator


class OpenAPISchemaGenerator(OpenAPISchemaGenerator):
   
   def determine_path_prefix(self, paths):
      return '/api/'

schema_view = get_schema_view(
   info=openapi.Info(
      title="Technology E-Commerce",
      default_version='v1',
      description="E-commerce API to project to freelancers buy, sell, and exchange technology products.",
   ),
   public=True,
   generator_class=OpenAPISchemaGenerator
)

urlpatterns = [
    # System urls
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^accounts/', include('rest_framework.urls')),
    
    # Project urls
    re_path(r'', include('apps.core.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    re_path(r'^api/(?P<version>(v1|v2))/users/', include('apps.users.urls'), name='Users'),
    re_path(r'^api/(?P<version>(v1|v2))/authenticate/', include('apps.authentication.urls'), name='Authenticate'),

    # Statics
    *staticfiles_urlpatterns()
]
