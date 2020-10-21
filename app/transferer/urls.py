from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework import permissions

API_PREFIX = 'api/'

schema_view = get_schema_view(
    openapi.Info(
        title="Transferer API",
        default_version='v1',
        description="",
        authentication_classes=[],
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{API_PREFIX}transactions/', include('transaction.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
