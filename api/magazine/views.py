from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from api.magazine.serializers import *
from .models import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class MagazinesListView(ListAPIView):
    serializer_class = MagazinesListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]
    ordering = ['-id']

    def get_queryset(self):
        magazines = Magazines.objects.filter(published=True)
        return magazines


class MagazineRetrieveView(RetrieveAPIView):
    serializer_class = MagazineRetrieveSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.hits += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        magazines = Magazines.objects.filter(published=True)
        return magazines


class MagazineLikeUpdateView(UpdateAPIView):
    queryset = Magazines.objects.prefetch_related('like_users').all()
    serializer_class = MagazineLikeSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ['put']
    lookup_field = 'id'


class MagazineReviewsListSerializer(ListAPIView):
    serializer_class = MagazineReviewsListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]
    ordering = ['-id']

    def get_queryset(self):
        magazine_comments = MagazineComments.objects.filter(magazines_id=self.kwargs['id'])
        return magazine_comments


class MagazineReviewCreateView(CreateAPIView):
    serializer_class = MagazineReviewSerializer


class MagazineReviewRetrieveUpdateRetrieveView(RetrieveUpdateDestroyAPIView):
    serializer_class = MagazineReviewSerializer
