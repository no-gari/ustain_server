from django.urls import path
from api.magazine.views import *

urlpatterns = [
    path('list/', MagazinesListView.as_view()),
    path('detail/<int:id>/', MagazineRetrieveView.as_view()),
    path('detail/<int:id>/update-like/', MagazineLikeUpdateView.as_view()),
    path('detail/<int:id>/reviews/', MagazineReviewsListSerializer.as_view()),
    path('detail/<int:id>/review-create/', MagazineReviewCreateView.as_view()),
    path('detail/<int:id>/review-read-update-delete/', MagazineReviewRetrieveUpdateRetrieveView.as_view()),
]