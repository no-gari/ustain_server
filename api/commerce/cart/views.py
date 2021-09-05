from api.commerce.cart.serializers import CartListSerializer, CartItemSerializer
from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView
from rest_framework.exceptions import ValidationError
from api.clayful_client import ClayfulCartClient
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class GetCartView(ListAPIView):
    serializer_class = CartListSerializer

    def get_queryset(self):
        try:
            clayful_cart_client = ClayfulCartClient(self.kwargs['clayful'])
            get_cart = clayful_cart_client.get_cart()
            if not get_cart.status == 200:
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
            return get_cart.data['cart']['items']
        except Exception as err:
            raise ValidationError({'error_msg': [err]})

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
        self.kwargs.update({'clayful': request.META.get('HTTP_CLAYFUL')})
        return self.list(request, *args, **kwargs)


class AddItemToCartView(CreateAPIView):
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        try:
            clayful_cart_client = ClayfulCartClient(self.kwargs['clayful'])
            add_item = clayful_cart_client.add_item(
                product_id=serializer.validated_data.get('product'),
                variant=serializer.validated_data.get('variant'),
                quantity=serializer.validated_data.get('quantity')
            )
            if not add_item.status == 200:
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
        except Exception as err:
            raise ValidationError({'error_msg': err})
        serializer.save(
            shipping_method=add_item.data['shippingMethod'],
            bundle_items=add_item.data['bundleItems'],
            added_at=add_item.data['addedAt'],
            id=add_item.data['_id'],
        )

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
        self.kwargs.update({'clayful': request.META.get('HTTP_CLAYFUL')})
        return self.create(request, *args, **kwargs)


class DeleteItemToCartView(DestroyAPIView):
    serializer_class = CartItemSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            clayful_cart_client = ClayfulCartClient(self.kwargs['clayful'])
            delete_item = clayful_cart_client.delete_item(item_id=self.kwargs['id'])
            if not delete_item.status == 204:
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            raise ValidationError({'error_msg': err})

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
        self.kwargs.update({'clayful': request.META.get('HTTP_CLAYFUL')})
        return self.destroy(request, *args, **kwargs)


@api_view(["DELETE"])
def empty_cart(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    clayful_cart_client = ClayfulCartClient(auth_token=request.header['clayful'])
    response = clayful_cart_client.empty_cart()
    if response.status == 204:
        return Response(response.data, status=status.HTTP_200_OK)
    else:
        raise ValidationError({'error_msg': '장바구니를 비우지 못했습니다. 다시 시도해주세요.'})


@api_view(["GET"])
def count_items(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    clayful_cart_client = ClayfulCartClient(auth_token=request.header['clayful'])
    response = clayful_cart_client.count_items_cart()
    if response.status == 200:
        return Response({'count': response.data['count']['formatted']}, status=status.HTTP_200_OK)
    else:
        raise ValidationError({'error_msg': '다시 시도해주세요.'})


@api_view(["POST"])
def checkout_cart(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    clayful_cart_client = ClayfulCartClient(auth_token=request.header['clayful'])
    response = clayful_cart_client.checkout_cart(items=request.data['items'], clayful=request.headers['clayful'])
    if response.status == 200:
        return Response({'count': response.data}, status=status.HTTP_200_OK)
    else:
        raise ValidationError({'error_msg': '다시 시도해주세요.'})
