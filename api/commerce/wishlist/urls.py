from django.urls import path
from api.commerce.wishlist.views import RetrieveWishListProductsView, AddProductToWishListView, DeleteProductFromWishListView

urlpatterns = [
    path('products/', RetrieveWishListProductsView.as_view()),
    path('add/product/', AddProductToWishListView.as_view()),
    path('delete/product/', DeleteProductFromWishListView.as_view()),
]
