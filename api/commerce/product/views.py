from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from api.clayful_client import ClayfulProductClient
from api.commerce.product.serializers import ProductListByCategoriesSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1


class ProductListByCategoriesView(ListAPIView):
    serializer_class = ProductListByCategoriesSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        try:
            mid = self.kwargs['mid']
        except KeyError:
            mid = 'any'

        # collection 이름에 해당하는 상품 가져오기
        clayful_product_client = ClayfulProductClient()
        try:
            list_categories = clayful_product_client.list_categories(collection=mid)

            if not list_categories.status == 200:
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
            else:
                return list_categories.data
        except Exception as err:
            raise ValidationError({'categories': ['%s: 유효하지 않은 id입니다.' % mid]})


class ProductDetailView(APIView):
    allowed_methods = ['get']

    def get(self, request, *args, **kwargs):
        # product id에 해당하는 상품 가져오기
        product_id = kwargs['id']
        clayful_product_client = ClayfulProductClient()
        try:
            product_detail = clayful_product_client.get_detail(id=product_id)

            if not product_detail.status == 200:
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
            else:
                return Response(product_detail.data)
        except Exception as err:
            raise ValidationError({'categories': ['%s: 유효하지 않은 id입니다.' % product_id]})