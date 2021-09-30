from api.commerce.cart.views import  empty_cart, count_items, GetCartView, AddItemToCartView, DeleteItemToCartView, add_to_cart
from django.urls import path

urlpatterns = [
    path('', GetCartView.as_view()),
    path('add/', add_to_cart),
    path('delete/<str:id>/', DeleteItemToCartView.as_view()),
    path('empty/', empty_cart),
    path('count-items/', count_items),
]