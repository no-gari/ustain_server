from api.commerce.cart.views import get_cart, add_to_cart, empty_cart, delete_item, count_items
from django.urls import path

urlpatterns = [
    path('', get_cart),
    path('add/', add_to_cart),
    path('empty/', empty_cart),
    path('delete-item/', delete_item),
    path('count-items/', count_items),
]