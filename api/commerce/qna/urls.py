from api.commerce.qna.views import qna_list, qna_count, get_qna, create_qna, delete_qna
from django.urls import path

urlpatterns = [
    path('list/<str:product>/', qna_list),
    path('count/<str:product>/', qna_count),
    path('detail/<str:review_id>/', get_qna),
    path('create/', create_qna),
    path('delete/', delete_qna),
]
