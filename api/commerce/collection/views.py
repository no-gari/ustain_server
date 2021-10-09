from api.commerce.collection.serializers import CollectionRetrieveSerializers
from rest_framework.decorators import api_view, permission_classes
from api.clayful_client import ClayfulCollectionClient
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


@api_view(["GET"])
@permission_classes([AllowAny])
def get_big_collections(request, *args, **kwargs):
    clayful_brand_client = ClayfulCollectionClient()
    try:
        response = clayful_brand_client.get_collections(parent=settings.CLAYFUL_PRODUCT_ID)
        large_categories = CollectionRetrieveSerializers(response.data, many=True).data
        big_categoreis = []
        if response.status == 200:
            for category in large_categories:
                categories = clayful_brand_client.get_collections(parent=category['_id'])
                big_categoreis.append({category['name']: CollectionRetrieveSerializers(categories.data, many=True).data})
            return Response(big_categoreis, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '카테고리를 가져오지 못했습니다.'})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_small_collections(request, *args, **kwargs):
    clayful_collection_client = ClayfulCollectionClient()
    try:
        small_collections = clayful_collection_client.get_collections(parent=kwargs['parent'])
        if small_collections.status == 200:
            serializer = CollectionRetrieveSerializers(small_collections.data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '카테고리를 가져오지 못했습니다.'})
