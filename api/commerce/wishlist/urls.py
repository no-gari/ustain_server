from django.urls import path
from api.commerce.wishlist.views import GetWishListProductsView, AddProductToWishListView, DeleteProductToWishListView

urlpatterns = [
    path('products/', GetWishListProductsView.as_view()),
    path('add/product/<str:product_id>/', AddProductToWishListView.as_view()),
    path('delete/product/<str:product_id>/', DeleteProductToWishListView.as_view()),
]