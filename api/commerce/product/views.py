from api.commerce.product.serializers import ProductListSerializer, ProductDetailSerializer
from rest_framework.exceptions import ValidationError
from api.clayful_client import ClayfulProductClient
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


class ProductListByCategoriesView(ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        mid = self.kwargs.get('mid', 'any')
        sort = self.request.query_params.get('sort', 'rating.count')
        clayful_product_client = ClayfulProductClient()
        try:
            list_categories = clayful_product_client.list_categories(collection=mid, sort=sort)
            if not list_categories.status == 200:
                raise ValidationError({'error_msg': '서버 에러입니다. 잠시 후 다시 시도해주세요.'})
            return list_categories.data
        except Exception:
            raise ValidationError({'error_msg': ['%s: 유효하지 않은 id입니다.' % mid]})


class ProductDetailView(APIView):
    allowed_methods = ['get']

    def get(self, request, *args, **kwargs):
        product_id = kwargs['id']
        clayful_product_client = ClayfulProductClient()
        try:
            product_detail = clayful_product_client.get_detail(id=product_id)
            if not product_detail.status == 200:
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
            else:
                serializer = ProductDetailSerializer(product_detail.data)
                return Response(serializer.data)
        except Exception as err:
            raise ValidationError({'error_msg': ['%s: 유효하지 않은 id입니다.' % product_id]})
