from django.urls import path, include

urlpatterns = [
    path('product/', include('api.commerce.product.urls')),
    path('wishlist/', include('api.commerce.wishlist.urls')),
    path('cart/', include('api.commerce.cart.urls')),
]