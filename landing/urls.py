from django.urls import path, include
from .views import RecieverView, receive_success, gifter, gift_success, GiftListView

urlpatterns = [
    path('recieve/<str:url>', RecieverView.as_view(), name='reciever'),
    path('recieve/success/', receive_success, name='recieve_success'),
    path('create/', gifter, name='gift_create'),
    path('create/success/', gift_success, name='gift_success'),
    path('list/', GiftListView.as_view(), name='gift_list'),
]
