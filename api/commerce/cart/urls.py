from api.commerce.cart.views import  empty_cart, count_items, add_to_cart, get_cart, delete_item
from django.urls import path

urlpatterns = [
    path('', get_cart),
    path('add/', add_to_cart),
    path('empty/', empty_cart),
    path('delete-item/', delete_item),
    path('count-items/', count_items),
]
