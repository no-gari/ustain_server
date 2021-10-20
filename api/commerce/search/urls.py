from api.commerce.search.views import search_list
from django.urls import path

urlpatterns = [
    path('<str:keyword>/', search_list),
]
