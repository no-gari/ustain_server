from api.commerce.order.views import order_create, order_create_instance, OrderListView, get_order, order_temp
from django.urls import path

urlpatterns = [
    path('create/', order_create),
    path('order-temp/', order_temp),
    path('<str:order_id>/', get_order),
    path('list/', OrderListView.as_view()),
    path('create-instance/', order_create_instance),
]
