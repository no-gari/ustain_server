from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, GenericAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from api.clayful_client import ClayfulCartClient
from api.commerce.cart.serializers import CartListSerializer, CartItemSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1


class GetCartView(ListAPIView):
    serializer_class = CartListSerializer
    # pagination_class = StandardResultsSetPagination

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            clayful_cart_client = ClayfulCartClient(self.kwargs['clayful'])
            get_cart = clayful_cart_client.get_cart()

            if not get_cart.status == 200:
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
            else:
                print(get_cart.data['cart']['items'])
                return get_cart.data['cart']['items']
        except Exception as err:
            raise ValidationError({'get_cart': [err]})

    def get(self, request, *args, **kwargs):
        self.kwargs.update({
            'clayful': request.META.get('HTTP_CLAYFUL')
        })
        return self.list(request, *args, **kwargs)


class AddItemToCartView(CreateAPIView):
    serializer_class = CartItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(serializer.validated_data)
        try:
            clayful_cart_client = ClayfulCartClient(self.kwargs['clayful'])
            add_item = clayful_cart_client.add_item(
                product_id=serializer.validated_data.get('product'),
                variant=serializer.validated_data.get('variant'),
                quantity=serializer.validated_data.get('quantity')
            )
            print(add_item.status)

            if not add_item.status == 200:
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
        except Exception as err:
            raise ValidationError({'add_product': err})
        print(add_item.data)
        serializer.save(
            shipping_method=add_item.data['shippingMethod'],
            bundle_items=add_item.data['bundleItems'],
            added_at=add_item.data['addedAt'],
            id=add_item.data['_id'],
        )

    def post(self, request, *args, **kwargs):
        self.kwargs.update({
            'clayful': request.META.get('HTTP_CLAYFUL')
        })
        return self.create(request, *args, **kwargs)


class DeleteItemToCartView(DestroyAPIView):
    serializer_class = CartItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            clayful_cart_client = ClayfulCartClient(self.kwargs['clayful'])
            delete_item = clayful_cart_client.delete_item(item_id=self.kwargs['id'])

            if not delete_item.status == 204:
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})

        except Exception as err:
            raise ValidationError({'add_product': err})

        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        self.kwargs.update({
            'clayful': request.META.get('HTTP_CLAYFUL')
        })
        return self.destroy(request, *args, **kwargs)

