from api.commerce.customer.views import AddressListView, AddressView, create_address, delete_address
from django.urls import path

urlpatterns = [
    path('address/list/', AddressListView.as_view()),
    path('address/<int:pk>/', AddressView.as_view()),
    path('address/create/', create_address),
    path('address/delete/', delete_address),
]
