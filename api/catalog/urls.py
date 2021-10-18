from api.catalog.views import catalog_list, get_catalog
from django.urls import path

urlpatterns = [
    path('list?page=<int:page>/', catalog_list),
    path('<str:catalog_id>/', get_catalog),
]
