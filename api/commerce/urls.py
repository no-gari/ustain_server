from django.urls import path, include

urlpatterns = [
    path('brand/', include('api.commerce.brand.urls')),
    path('cart/', include('api.commerce.cart.urls')),
    path('qna/', include('api.commerce.qna.urls')),
    path('comment/', include('api.commerce.comment.urls')),
    path('review/', include('api.commerce.review.urls')),
    path('product/', include('api.commerce.product.urls')),
    path('wishlist/', include('api.commerce.wishlist.urls')),
    path('cart/', include('api.commerce.cart.urls')),
]