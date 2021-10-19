from api.clayful_client import ClayfulCollectionClient, ClayfulProductClient
from api.commerce.product.serializers import ProductListSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from django.utils.html import strip_tags
from django.conf import settings


@api_view(["GET"])
def catalog_list(request, *args, **kwargs):
    try:
        clf_collection_client = ClayfulCollectionClient()
        clf_product_client = ClayfulProductClient()
        catalogs = []
        catalog_list = clf_collection_client.get_collections(parent=settings.CLAYFUL_CATALOG_ID).data
        for catalog in catalog_list:
            products = clf_product_client.list_products(page=kwargs.get('page', 1), collection=catalog['_id']).data
            if not products == []:
                serialized_products = ProductListSerializer(products, many=True).data[:3]
                catalogs.append({'Id': catalog.get('_id', None), 'name': catalog.get('name', None),
                                 'description': strip_tags(catalog.get('description', None)),
                                 'products': serialized_products})
        return Response(catalogs, status=HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '카탈로그를 불러올 수 없습니다.'})


@api_view(["GET"])
def get_catalog(request, *args, **kwargs):
    try:
        clf_collection_client = ClayfulCollectionClient()
        clf_product_client = ClayfulProductClient()
        collection_response = clf_collection_client.get_collection(parent=kwargs['catalog_id']).data
        product_response = clf_product_client.list_catalog_products(collection=kwargs['catalog_id'])
        serialized_products = ProductListSerializer(product_response.data, many=True).data
        return Response({'name': collection_response['name'],
                         'description': strip_tags(collection_response['description']),
                         'products': serialized_products}, status=HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '카탈로그를 불러올 수 없습니다.'})
