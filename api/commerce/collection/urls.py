from django.urls import path
from api.commerce.collection.views import get_big_collections, get_small_collections

urlpatterns = [
    path('', get_big_collections),
    path('<str:parent>/', get_small_collections),
]
