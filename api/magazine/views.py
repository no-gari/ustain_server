from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from api.magazine.serializers import *


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class MagazinesListView(ListAPIView):
    serializer_class = MagazinesListSerializer
    pagination_class = StandardResultsSetPagination


class MagazineRetrieveView(RetrieveAPIView):
    serializer_class = MagazineRetrieveSerializer


class MagazineLikeCreateView(CreateAPIView):
    serializer_class = MagazineLikeCreateSerializer


class MagazineLikeDeleteView(DestroyAPIView):
    serializer_class = MagazineLikeDeleteSerializer


class MagazineReviewsListSerializer(ListAPIView):
    serializer_class = MagazineReviewsListSerializer
    pagination_class = StandardResultsSetPagination


class MagazineReviewCreateView(CreateAPIView):
    serializer_class = MagazineReviewSerializer


class MagazineReviewRetrieveUpdateRetrieveView(RetrieveUpdateDestroyAPIView):
    serializer_class = MagazineReviewSerializer
