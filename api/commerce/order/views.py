from api.commerce.order.serializers import QueryOptionSerializer, OrderSerializer, PaymentSerializer
from api.clayful_client import ClayfulOrderClient, ClayfulCartClient
from rest_framework.exceptions import ValidationError
from api.commerce.list_helper import get_index
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


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


@api_view(["GET"])
def order_list(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        page = kwargs.get('page', 1)
        clf_order_client = ClayfulOrderClient(auth_token=request.META['HTTP_CLAYFUL'])
        order_count = clf_order_client.order_count().data
        max_index, previous, next_val = get_index(request, order_count['count']['raw'], page)
        order = clf_order_client.get_order_list(page=page)
        if order.status == 200:
            return Response(
                {'previous': previous, 'next': next_val, 'count': 10, 'results': order.data}, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '주문 내역을 불러올 수 없습니다.'})


@api_view(["GET"])
def get_order(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        clf_order_client = ClayfulOrderClient(auth_token=request.META['HTTP_CLAYFUL'])
        order = clf_order_client.get_order(order_id=kwargs['order_id'])
        if order.status == 200:
            return Response(order.data, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '주문 내역을 불러올 수 없습니다.'})
