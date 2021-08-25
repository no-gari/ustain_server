from django.urls import path
from api.commerce.brand.views import get_brand

urlpatterns = [
    path('<str:brand_id>', get_brand),
]