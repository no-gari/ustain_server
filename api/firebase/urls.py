from django.urls import path
from .viewsets import PushTokenAPIView

urlpatterns = [
    path('push/', PushTokenAPIView.as_view()),

]