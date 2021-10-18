from api.commerce.cart.serializers import CartListSerializer, CartItemSerializer
from rest_framework.exceptions import ValidationError
from api.clayful_client import ClayfulCartClient
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def get_cart(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        clayful_cart_client = ClayfulCartClient(auth_token=request.META['HTTP_CLAYFUL'])
        my_cart = clayful_cart_client.get_cart()
        if not my_cart.status == 200:
            raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
        if not my_cart.data['cart']['items'] == []:
            serializer = CartListSerializer(my_cart.data['cart']['items'], many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '장바구니를 불러오지 못했습니다. 다시 시도해주세요.'})


@api_view(["POST"])
def add_to_cart(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        added_list = []
        clayful_cart_client = ClayfulCartClient(auth_token=request.META['HTTP_CLAYFUL'])
        for data in request.data:
            response = clayful_cart_client.add_item(
                product_id=data.get('product'),
                variant=data.get('variant'),
                quantity=data.get('quantity')
            )
            if response.status != 200:
                raise ValidationError({'error_msg': '상품 추가에 실패했습니다.'})
            added_list.append(response.data)
        serializer = CartItemSerializer(added_list, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '다시 시도해주세요.'})


@api_view(["DELETE"])
def delete_item(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        clayful_cart_client = ClayfulCartClient(auth_token=request.META['HTTP_CLAYFUL'])
        for data in request.data:
            response = clayful_cart_client.delete_item(item_id=data['item_id'])
            if not response.status == 204:
                raise ValidationError({'error_msg': '품목을 삭제하지 못했습니다. 다시 시도해주세요.'})
        return Response(status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '품목을 삭제하지 못했습니다. 다시 시도해주세요.'})


@api_view(["DELETE"])
def empty_cart(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    clayful_cart_client = ClayfulCartClient(auth_token=request.META['HTTP_CLAYFUL'])
    try:
        response = clayful_cart_client.empty_cart()
        if response.status == 204:
            return Response(response.data, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '장바구니를 비우지 못했습니다. 다시 시도해주세요.'})


@api_view(["GET"])
def count_items(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    clayful_cart_client = ClayfulCartClient(auth_token=request.META['HTTP_CLAYFUL'])
    try:
        response = clayful_cart_client.count_items_cart()
        if response.status == 200:
            return Response(response.data['count']['raw'], status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '다시 시도해주세요.'})
