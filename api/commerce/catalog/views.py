from api.commerce.catalog.serializers import CatalogSortSerilaizer, CatalogListSerializer, CatalogDetailSerializer
from api.clayful_client import ClayfulCollectionClient, ClayfulProductClient
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from django.conf import settings


@api_view(["GET"])
def catalog_list(request, *args, **kwargs):
    try:
        clf_collection_client = ClayfulCollectionClient()
        clf_collection = clf_collection_client.get_collections(parent=settings.CLAYFUL_CATALOG_ID)
        collection_serializer_data = CatalogSortSerilaizer(clf_collection.data, many=True).data
        clf_product_client = ClayfulProductClient()
        product_data = []
        for collection_data in collection_serializer_data:
            product_data.append(clf_product_client.list_products())

        return Response(product_data, status=HTTP_200_OK)
    except:
        return ValidationError({'error_msg': '카탈로그를 불러올 수 없습니다.'})


@api_view(["GET"])
def get_catalog(request, *args, **kwargs):
    pass