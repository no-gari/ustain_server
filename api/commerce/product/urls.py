from api.commerce.product.views import ProductListByCategoriesView, ProductDetailView
from django.urls import path

urlpatterns = [
    path('<str:category>/list/', ProductListByCategoriesView.as_view()),
    path('list/', ProductListByCategoriesView.as_view()),
    path('detail/<str:id>/', ProductDetailView.as_view())
    # path('brand/<str:brand>/', ProductListByCategoriesView.as_view()),
]
