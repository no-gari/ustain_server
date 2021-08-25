from django.urls import path, include

urlpatterns = [
    path('brand/', include('api.commerce.brand.urls')),
    path('cart/', include('api.commerce.cart.urls')),
    path('product/', include('api.commerce.product.urls')),
]