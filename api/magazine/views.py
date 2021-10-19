from rest_framework.generics import UpdateAPIView, CreateAPIView, ListAPIView, RetrieveAPIView, \
    DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from api.magazine.serializers import *
from .models import *


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class MagazinesListView(ListAPIView):
    serializer_class = MagazinesListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        categories = eval(self.request.query_params.get('categories', []))
        if categories != []:
            magazines = Magazines.objects.filter(published=True, categories__in=categories).order_by('-id')
        else:
            magazines = Magazines.objects.filter(published=True).order_by('-id')
        return magazines


class LikeMagazinesListView(ListAPIView):
    serializer_class = MagazinesListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        magazines = user.like_magazines.all().filter(published=True).order_by('-id')
        return magazines


class ScrappedMagazinesListView(ListAPIView):
    serializer_class = MagazinesListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        magazines = user.scrapped_magazines.all().filter(published=True).order_by('-id')
        return magazines


class MainMagazinesListView(ListAPIView):
    serializer_class = MagazinesListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        magazines = Magazines.objects.filter(published=True, is_main=True).order_by('-id')
        return magazines


class MainBannerMagazineListView(ListAPIView):
    serializer_class = MagazinesListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        magazines = Magazines.objects.filter(published=False, is_banner=True).order_by('-id')
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


class MagazineLikeUpdateView(RetrieveUpdateAPIView):
    queryset = Magazines.objects.prefetch_related('like_users').all()
    serializer_class = MagazineLikeSerializer
    permission_classes = [AllowAny]
    allowed_methods = ['put', 'get']
    lookup_field = 'id'


class MagazineScrapUpdateView(RetrieveUpdateAPIView):
    queryset = Magazines.objects.prefetch_related('scrapped_users').all()
    serializer_class = MagazineScrapUpdateSerializer
    permission_classes = [AllowAny]
    allowed_methods = ['put', 'get']
    lookup_field = 'id'


class MagazineReviewsListSerializer(ListAPIView):
    serializer_class = MagazineReviewsListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        magazine_comments = MagazineComments.objects.filter(magazines_id=self.kwargs['id'], parent=None).order_by('id')
        return magazine_comments


class MagazineReviewCreateView(CreateAPIView):
    serializer_class = MagazineReviewCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'status': 200, 'data': response.data})


class MagazineCommentUpdateView(UpdateAPIView):
    serializer_class = MagazineReviewUpdateSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ['put']
    lookup_field = 'id'

    def get_object(self):
        instance = MagazineComments.objects.get(id=self.kwargs['id'])
        if instance.user != self.request.user:
            raise ValidationError({'error_msg': '댓글 작성자 본인만 수정할 수 있습니다.'})
        return instance


class MagazineCommentDeleteView(DestroyAPIView):
    serializer_class = MagazineReviewDestroySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_object(self):
        instance = MagazineComments.objects.get(id=self.kwargs['id'])
        if instance.user != self.request.user:
            raise ValidationError({'error_msg': '댓글 작성자 본인만 삭제할 수 있습니다.'})
        return instance

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({'status': 200, 'data': response.data})
