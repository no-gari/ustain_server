from django.urls import path, include

urlpatterns = [
    path('cart/', include('api.commerce.cart.urls')),
    path('brand/', include('api.commerce.brand.urls')),
    path('order/', include('api.commerce.order.urls')),
    path('review/', include('api.commerce.review.urls')),
    path('coupon/', include('api.commerce.coupon.urls')),
    path('search/', include('api.commerce.search.urls')),
    path('comment/', include('api.commerce.comment.urls')),
    path('product/', include('api.commerce.product.urls')),
    path('catalog/', include('api.commerce.catalog.urls')),
    path('customer/', include('api.commerce.customer.urls')),
    path('collection/', include('api.commerce.collection.urls')),
]
