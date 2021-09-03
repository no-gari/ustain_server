from api.commerce.product.serializers import ProductListSerializer, ProductDetailSerializer
from rest_framework.exceptions import ValidationError
from api.clayful_client import ClayfulProductClient
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class ProductListByCategoriesView(ListAPIView):
    def get_queryset(self):
        try:
            brand = self.kwargs.get('brand', 'any')
            category = self.kwargs.get('category', 'any')
            sort = self.request.query_params.get('sort', 'rating.count')
            clayful_product_client = ClayfulProductClient()
            products = clayful_product_client.list_products(collection=category, sort=sort, brand=brand)
            if not products.status == 200:
                raise ValidationError({'error_msg': '서버 에러입니다. 잠시 후 다시 시도해주세요.'})
            return products.data
        except Exception:
            raise ValidationError({'error_msg': '상품을 불러올 수 없습니다.'})

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            brand = self.kwargs.get('brand', 'any')
            category = self.kwargs.get('category', 'any')
            clayful_wishlist_client = ClayfulProductClient()
            wishlist_count = clayful_wishlist_client.count_products(collection=category, brand=brand)
            max_index = int(wishlist_count.data['count']['formatted']) // 10 + 1
            serializer = ProductListSerializer(queryset, many=True)
            response = {'max_index': max_index, 'products': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception:
            raise ValidationError({'error_msg': '상품을 불러올 수 없습니다.'})


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
