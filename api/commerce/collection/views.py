from rest_framework.decorators import api_view, permission_classes
from api.clayful_client import ClayfulCollectionClient
from .serializers import CollectionRetrieveSerializers
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
@permission_classes([AllowAny])
def get_big_collections(request, *args, **kwargs):
    clayful_brand_client = ClayfulCollectionClient()
    response = clayful_brand_client.get_collections()
    if response.status == 200:
        serializer = CollectionRetrieveSerializers(response.data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        raise ValidationError({'error_msg': '카테고리를 가져오지 못했습니다.'})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_small_collections(request, *args, **kwargs):
    clayful_collection_client = ClayfulCollectionClient()
    small_collections = clayful_collection_client.get_collections(parent=kwargs['parent'])
    if small_collections.status == 200:
        serializer = CollectionRetrieveSerializers(small_collections.data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        raise ValidationError({'error_msg': '카테고리를 가져오지 못했습니다.'})
