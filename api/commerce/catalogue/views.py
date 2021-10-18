from api.clayful_client import ClayfulCollectionClient
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


@api_view(["GET"])
def catalogue_list(request, *args, **kwargs):
    try:
        clayful_comment_client = ClayfulCollectionClient()
        response = clayful_comment_client.get_collection(parent=settings.CLAYFUL_CATALOGUE_ID)
        return Response(response.data, status=status.HTTP_200_OK)
    except:
        return ValidationError({'error_msg': '카탈로그를 불러올 수 없습니다.'})


@api_view(["GET"])
def get_catalogue(request, *args, **kwargs):
    pass