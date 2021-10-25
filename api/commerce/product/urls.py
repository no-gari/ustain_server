from api.commerce.product.views import ProductListByCategoriesView, ProductDetailView, order_temp
from django.urls import path

urlpatterns = [
    path('<str:category>/list/', ProductListByCategoriesView.as_view()),
    path('list/', ProductListByCategoriesView.as_view()),
    path('detail/<str:id>/', ProductDetailView.as_view()),
    path('order-temp/', order_temp),
    # path('brand/<str:brand>/', ProductListByCategoriesView.as_view()),
]
