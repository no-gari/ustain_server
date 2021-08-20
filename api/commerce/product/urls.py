from django.urls import path
from api.commerce.product.views import ProductListByCategoriesView

urlpatterns = [
    path('list/categories/', ProductListByCategoriesView.as_view())
]