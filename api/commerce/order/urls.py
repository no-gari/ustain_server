from api.commerce.order.views import order_create, order_list, get_order, order_temp, order_cancel
from django.urls import path

urlpatterns = [
    path('list/', order_list),
    path('create/', order_create),
    path('cancel/', order_cancel),
    path('order-temp/', order_temp),
    path('<str:order_id>/', get_order),
]
