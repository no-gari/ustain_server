from django.urls import path
from api.magazine.views import *

urlpatterns = [
    path('magazines-list/', MagazinesListView.as_view()),
    path('magazine/<int:id>/', MagazineRetrieveView.as_view()),
    path('magazine/<int:id>/like-users/', MagazineLikeUserListView.as_view()),
    path('magazine/<int:id>/create-like/', MagazineLikeCreateView.as_view()),
    path('magazine/<int:id>/delete-like/', MagazineLikeDeleteView.as_view()),
    path('magazine/<int:id>/reviews/', MagazineReviewsListSerializer.as_view()),
    path('magazine/<int:id>/review-create/', MagazineReviewCreateView.as_view()),
    path('magazine/<int:id>/review-read-update-delete/', MagazineReviewRetrieveUpdateRetrieveView.as_view()),
]