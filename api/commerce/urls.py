from django.urls import path, include

urlpatterns = [
    path('qna/', include('api.commerce.qna.urls')),
    path('cart/', include('api.commerce.cart.urls')),
    path('cart/', include('api.commerce.cart.urls')),
    path('brand/', include('api.commerce.brand.urls')),
    path('review/', include('api.commerce.review.urls')),
    path('comment/', include('api.commerce.comment.urls')),
    path('product/', include('api.commerce.product.urls')),
    path('wishlist/', include('api.commerce.wishlist.urls')),
    path('collection/', include('api.commerce.collection.urls')),
]