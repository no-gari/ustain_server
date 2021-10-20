from api.commerce.product.serializers import ProductListSerializer
from api.magazine.serializers import MagazinesListSerializer
from rest_framework.exceptions import ValidationError
from api.clayful_client import ClayfulProductClient
from rest_framework.decorators import api_view
from api.commerce.list_helper import get_index
from rest_framework.response import Response
from api.magazine.models import Magazines
from rest_framework import status


@api_view(["GET"])
def search_list(request, *args, **kwargs):
    try:
        keyword = kwargs.get('keyword')
        page = kwargs.get('page', 1)
        if keyword.strip() == '':
            raise ValidationError({'error_msg': '검색어를 입력 해주세요.'})
        clf_product_client = ClayfulProductClient()
        product_response = clf_product_client.search_products(keyword=keyword, page=page).data
        product_count = clf_product_client.search_products_count(keyword=keyword).data['count']['raw']
        max_index, previous, next_val = get_index(request, product_count, page)
        serialized_products = ProductListSerializer(product_response, many=True)
        magazine_response = Magazines.objects.filter(title__contains=keyword, published=True)
        serialized_magazines = MagazinesListSerializer(magazine_response, many=True)
        return Response(
            {'previous': previous, 'next': next_val, 'count': 10, 'results':
                {'products': serialized_products.data, 'magazines': serialized_magazines.data}}, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '다시 한 번 시도 해주세요.'})
