from api.catalog.serializers import CatalogListSerializers, CatalogRetrieveSerializer
from api.clayful_client import ClayfulCollectionClient, ClayfulProductClient
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from api.commerce.list_helper import get_index_catalog
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from django.conf import settings


@api_view(["GET"])
def catalog_list(request, *args, **kwargs):
    try:
        clf_colleciton = ClayfulCollectionClient()
        clf_catalogs = ClayfulCollectionClient.get_collections(parent=settings.CLAYFUL_CATALOG_ID).data
        return Response(clf_catalogs, status=HTTP_200_OK)

    except:
        raise ValidationError({'error_msg': '카탈로그 불러오기를 실패했습니다.'})


@api_view(["GET"])
def get_catalog(request, *args, **kwargs):
    try:
        catalog_id = kwargs['catalog_id']

    except:
        raise ValidationError({'error_msg': '카탈로그 불러오기를 실패했습니다.'})
