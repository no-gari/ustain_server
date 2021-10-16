from api.commerce.order.serializers import QueryOptionSerializer, OrderSerializer, PaymentSerializer
from api.commerce.customer.serializers import AddressSerializer, ShippingrRequestSerializers
from api.commerce.product.serializers import ProductCheckoutSerializer

from api.clayful_client import ClayfulOrderClient, ClayfulCartClient, ClayfulProductClient
from api.commerce.customer.models import UserShipping, ShippingRequest
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from api.commerce.list_helper import get_index
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
def order_temp(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        if type(request.data) != list:
            clf_product_client = ClayfulProductClient()
            data = clf_product_client.get_detail(id=request.data['product']).data
            serialized_data = [ProductCheckoutSerializer(
                {'products': data, 'variant': request.data['variant'], 'quantity': request.data['quantity']}).data]
        else:
            serialized_data = request.data
        address = UserShipping.objects.filter(is_default=True, user=request.user).first()
        serialized_address = AddressSerializer(address).data
        serialized_requests = ShippingrRequestSerializers(ShippingRequest.objects.all(), many=True).data
        return Response({'products': serialized_data, 'address': serialized_address,
                         'request': {'shipping_request': serialized_requests, 'additional_request': ''},
                         'coupon': {'Id': None, 'name': None, 'description': None, 'min_price': None, 'discount': None,
                                    'expires_at': None}, 'agreed': False}, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '상품 에러입니다.'})


@api_view(["POST"])
def order_create(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        clf_client = ClayfulCartClient(auth_token=request.META['HTTP_CLAYFUL'])
        first = request.data['products'][0]
        if first['_id'] is None:
            add = clf_client.add_item(product_id=first['product_id'], variant=first['variant_id'], quantity=first['quantity'])
            items = add.data['_id']
        else:
            items = QueryOptionSerializer(request.data['products'])
        payload = OrderSerializer(request.data).data
        response = clf_client.checkout_cart(items=items, payload=payload)
        if response.status == 201:
            return Response(PaymentSerializer(response.data['order']).data, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '주문에 실패했습니다.'})


@api_view(["POST"])
def order_cancel(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        clf_client = ClayfulOrderClient(auth_token=request.META['HTTP_CLAYFUL'])
        order_id, payload = request.data['merchant_uid'], {'reason': '...'}
        response = clf_client.order_cancel(order_id=order_id, payload=payload)
        if response.status == 200:
            return Response(status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '주문 취소에 실패했습니다.'})


class OrderListView(ListAPIView):
    def get_queryset(self):
        try:
            clayful_order_client = ClayfulOrderClient()
            products = clayful_order_client.get_order_list(clayful=self.request.META['HTTP_CLAYFUL'])
            if not products.status == 200:
                raise ValidationError({'error_msg': '서버 에러입니다. 잠시 후 다시 시도해주세요.'})
            return products.data
        except Exception:
            raise ValidationError({'error_msg': '주문 내역을 불러올 수 없습니다.'})

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            page = self.kwargs.get('page', 1)
            clf_order_client = ClayfulOrderClient()
            order_count = clf_order_client.order_count(clayful=request.META['HTTP_CLAYFUL']).data
            max_index, previous, next_val = get_index(request, order_count['count']['raw'], page)
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
            raise ValidationError({'error_msg': '주문 내역을 불러올 수 없습니다.'})


@api_view(["GET"])
def get_order(request, *args, **kwargs):
    pass
