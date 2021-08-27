from api.commerce.comment.views import get_comments
from django.urls import path

urlpatterns = [
    path('', get_comments),
]