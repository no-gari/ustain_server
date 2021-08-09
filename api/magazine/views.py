from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from api.magazine.serializers import *


class MagazinesListView(ListAPIView):
    serializer_class = MagazinesListSerializer


class MagazineRetrieveView(RetrieveAPIView):
    serializer_class = MagazineRetrieveSerializer


class MagazineLikeCreateView(CreateAPIView):
    serializer_class = MagazineLikeCreateSerializer


class MagazineLikeDeleteView(DestroyAPIView):
    serializer_class = MagazineLikeDeleteSerializer


class MagazineReviewsListSerializer(ListAPIView):
    serializer_class = MagazineReviewsListSerializer


class MagazineReviewCreateView(CreateAPIView):
    serializer_class = MagazineReviewSerializer


class MagazineReviewRetrieveUpdateRetrieveView(RetrieveUpdateDestroyAPIView):
    serializer_class = MagazineReviewSerializer
