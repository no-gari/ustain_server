from api.catalog.serializers import CatalogListSerializers, CatalogRetrieveSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from api.catalog.models import Catalog


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class CatalogsListView(ListAPIView):
    serializer_class = CatalogListSerializers
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        categories = eval(self.request.query_params.get('categories', []))
        if categories != []:
            magazines = Catalog.objects.filter(published=True, categories__in=categories).order_by('-id')
        else:
            magazines = Catalog.objects.filter(published=True).order_by('-id')
        return magazines


class CatalogRetrieveView(RetrieveAPIView):
    serializer_class = CatalogRetrieveSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.hits += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        magazines = Catalog.objects.filter(published=True)
        return magazines
