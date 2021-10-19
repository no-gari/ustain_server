from api.commerce.catalog.views import get_catalog, catalog_list
from django.urls import path

urlpatterns = [
    path('list/', catalog_list),
    path('<str:catalog_id>/', get_catalog),
]
