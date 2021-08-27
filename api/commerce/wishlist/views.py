from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from api.clayful_client import ClayfulWishListClient
from api.commerce.wishlist.serializers import GetWishListProductsSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1


class GetWishListProductsView(ListAPIView):
    serializer_class = GetWishListProductsSerializer
    pagination_class = StandardResultsSetPagination

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            clayful_wishlist_client = ClayfulWishListClient(self.kwargs['clayful'])
            list_products = clayful_wishlist_client.get_list_products()

            if not list_products.status == 200:
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
            else:
                return list_products.data
        except Exception as err:
            raise ValidationError({'wishlist_products': [err]})

    def get(self, request, *args, **kwargs):
        self.kwargs.update({
            'clayful': request.META.get('HTTP_CLAYFUL')
        })
        return self.list(request, *args, kwargs)


class AddProductToWishListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    allowed_methods = ['get']

    def get(self, request, *args, **kwargs):
        self.kwargs.update({
            'clayful': request.META.get('HTTP_CLAYFUL')
        })
        try:
            clayful_wishlist_client = ClayfulWishListClient(self.kwargs['clayful'])
            add_item = clayful_wishlist_client.add_item(product_id=self.kwargs['product_id'])

            print(add_item.status)

            if not add_item.status == 200:
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})

        except Exception as err:
            raise ValidationError({'add_product': err})

        return Response(add_item.data)


class DeleteProductToWishListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    allowed_methods = ['delete']

    def delete(self, request, *args, **kwargs):
        self.kwargs.update({
            'clayful': request.META.get('HTTP_CLAYFUL')
        })
        try:
            clayful_wishlist_client = ClayfulWishListClient(self.kwargs['clayful'])
            delete_item = clayful_wishlist_client.delete_item(product_id=self.kwargs['product_id'])

            if not delete_item.status == 204:
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
            else:
                return Response(delete_item.data, status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            raise ValidationError({'delete_product': err})
