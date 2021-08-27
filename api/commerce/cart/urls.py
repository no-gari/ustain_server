from django.urls import path
from api.commerce.cart.views import GetCartView, AddItemToCartView, DeleteItemToCartView

urlpatterns = [
    path('', GetCartView.as_view()),
    path('add/item/', AddItemToCartView.as_view()),
    path('delete/item/<str:id>/', DeleteItemToCartView.as_view()),
]