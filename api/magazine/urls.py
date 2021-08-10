from django.urls import path
from api.magazine.views import *

urlpatterns = [
    path('list/', MagazinesListView.as_view()),
    path('<int:id>/', MagazineRetrieveView.as_view()),
    path('<int:id>/create-like/', MagazineLikeCreateView.as_view()),
    path('<int:id>/delete-like/', MagazineLikeDeleteView.as_view()),
    path('<int:id>/reviews/', MagazineReviewsListSerializer.as_view()),
    path('<int:id>/review-create/', MagazineReviewCreateView.as_view()),
    path('<int:id>/review-read-update-delete/', MagazineReviewRetrieveUpdateRetrieveView.as_view()),
]