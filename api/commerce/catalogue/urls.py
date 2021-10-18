from api.commerce.catalogue.views import catalogue_list, get_catalogue
from django.urls import path

urlpatterns = [
    path('list/', get_catalogues),
    path('<str:catalogue_id>', get_catalogues),
]
