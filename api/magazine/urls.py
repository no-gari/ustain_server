from api.magazine.views import *
from django.urls import path

urlpatterns = [
    path('list/', MagazinesListView.as_view()),
    path('list/is-main/', MainMagazinesListView.as_view()),
    path('detail/<int:id>/', MagazineRetrieveView.as_view()),
    path('list/scrapped/', ScrappedMagazinesListView.as_view()),
    path('detail/<int:id>/update-like/', MagazineLikeUpdateView.as_view()),
    path('detail/<int:id>/update-scrap/', MagazineScrapUpdateView.as_view()),
    path('detail/<int:id>/reviews/', MagazineReviewsListSerializer.as_view()),
    path('detail/reviews/review-create/', MagazineReviewCreateView.as_view()),
    path('detail/<int:id>/review/update/', MagazineCommentUpdateView.as_view()),
    path('detail/<int:id>/review/delete/', MagazineCommentDeleteView.as_view()),
]