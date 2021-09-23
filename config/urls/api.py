from django.conf import settings
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.contrib import admin
from django.conf.urls.static import static


schema_view = get_schema_view(
    openapi.Info(
        title=f'{settings.SITE_NAME} API',
        default_version='v1',
        description="Test description",
    ),
    public=False,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    path('', include('landing.urls')),
    path('api/v1/', include('api.urls')),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = f'{settings.SITE_NAME} Admin'
admin.site.site_title = f'{settings.SITE_NAME}'
