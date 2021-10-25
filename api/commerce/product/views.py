from api.commerce.product.serializers import ProductListSerializer, ProductDetailSerializer, ProductCheckoutSerializer
from api.commerce.customer.serializers import AddressSerializer, ShippingrRequestSerializers
from api.commerce.customer.models import UserShipping, ShippingRequest
from rest_framework.exceptions import ValidationError
from api.clayful_client import ClayfulProductClient
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from api.commerce.list_helper import get_index
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
            page = self.kwargs.get('page', 1)
            clf_product_client = ClayfulProductClient()
            products_count = clf_product_client.count_products(collection=category, brand=brand).data
            max_index, previous, next_val = get_index(request, products_count['count']['raw'], page)
            serializer = ProductListSerializer(queryset, many=True)
            if not serializer.data == []:
                response = {'previous': previous, 'next': next_val, 'count': 10, 'results': serializer.data}
            else:
                response = {
                    'previous': None, 'next': None, 'count': None,
                    'result': {
                        '_id': None, 'name': None, 'hashtags': None, 'rating': None, 'original_price': None,
                        'discount_price': None, 'discount_rate': None, 'brand': None, 'thumbnail': None
                    }
                }
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
                return Response(serializer.data, status=status.HTTP_200_OK)
                # return Response(product_detail.data, status=status.HTTP_200_OK)
        except Exception:
            raise ValidationError({'error_msg': '유효하지 않은 id입니다.'})


@api_view(["POST"])
def order_temp(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        clf_product_client = ClayfulProductClient()
        product_list = []
        for data in request.data:
            product = clf_product_client.get_detail(id=data['product']).data
            serialized_data = ProductCheckoutSerializer(
                {'products': product, 'variant': data['variant'], 'quantity': data['quantity']}).data
            product_list.append(serialized_data)
        address = UserShipping.objects.filter(is_default=True, user=request.user).first()
        serialized_address = AddressSerializer(address).data
        serialized_requests = ShippingrRequestSerializers(ShippingRequest.objects.all(), many=True).data
        return Response({'products': product_list, 'address': serialized_address,
                         'request': {'shipping_request': serialized_requests, 'additional_request': ''},
                         'coupon': {'Id': None, 'name': None, 'description': None, 'min_price': None,
                                    'discount': None, 'expires_at': None}}, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '상품 에러입니다.'})
