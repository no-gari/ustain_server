from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('', admin.site.urls),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
]


urlpatterns += static(settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = f'{settings.SITE_NAME} Administration'
admin.site.site_title = f'{settings.SITE_NAME}'
