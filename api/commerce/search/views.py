from api.commerce.product.serializers import ProductListSerializer
from api.magazine.serializers import MagazinesListSerializer
from rest_framework.exceptions import ValidationError
from api.clayful_client import ClayfulProductClient
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.magazine.models import Magazines
from rest_framework import status


@api_view(["GET"])
def search_list(request, *args, **kwargs):
    try:
        keyword = kwargs.get('keyword')
        if keyword.strip() == '':
            raise ValidationError({'error_msg': '검색어를 입력 해주세요.'})
        clf_product_client = ClayfulProductClient()
        product_response = clf_product_client.list_products().data



    except:
        raise ValidationError({'error_msg': '다시 한 번 시도 해주세요.'})
