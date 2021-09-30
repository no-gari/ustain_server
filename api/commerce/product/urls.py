from django.urls import path
from api.commerce.product.views import ProductListByCategoriesView, ProductDetailView

urlpatterns = [
    path('<str:category>/list/', ProductListByCategoriesView.as_view()),
    path('list/', ProductListByCategoriesView.as_view()),
    path('brand/<str:brand>/', ProductListByCategoriesView.as_view()),
    path('detail/<str:id>/', ProductDetailView.as_view())
]