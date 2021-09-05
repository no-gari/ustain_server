from rest_framework_simplejwt.authentication import JWTAuthentication
from api.commerce.product.serializers import ProductListSerializer
from rest_framework.exceptions import ValidationError
from api.clayful_client import ClayfulWishListClient
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class RetrieveWishListProductsView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    allowed_methods = ['get']

    def get_queryset(self):
        try:
            clayful_wishlist_client = ClayfulWishListClient(clayful=self.kwargs['clayful'])
            list_products = clayful_wishlist_client.get_list_products(
                page=int(self.request.query_params['page']), clayful=self.kwargs['clayful'])
            if not list_products.status == 200:
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
            else:
                return list_products.data
        except Exception as errors:
            raise ValidationError({'error_msg': [errors.args]})

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
        self.kwargs.update({'clayful': request.META.get('HTTP_CLAYFUL')})
        return self.list(request, *args, kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        clayful_wishlist_client = ClayfulWishListClient(clayful=self.kwargs['clayful'])
        wishlist_count = clayful_wishlist_client.count_wishlist()
        max_index = int(wishlist_count.data['count']['formatted']) // 10 + 1
        serializer = ProductListSerializer(queryset, many=True)
        response = {'max_index': max_index, 'products': serializer.data}
        return Response(response, status=status.HTTP_200_OK)


class AddProductToWishListView(APIView):
    authentication_classes = [JWTAuthentication]
    allowed_methods = ['post']

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
        self.kwargs.update({'clayful': request.META.get('HTTP_CLAYFUL')})
        try:
            clayful_wishlist_client = ClayfulWishListClient(clayful=self.kwargs['clayful'])
            add_item = clayful_wishlist_client.add_item(product_id=request.POST['product_id'])
            if not add_item.status == 200:
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
        except Exception as errrors:
            raise ValidationError({'error_msg': errrors.args[0]['add_item'][0]})
        return Response(add_item.data, status=status.HTTP_200_OK)


class DeleteProductFromWishListView(APIView):
    authentication_classes = [JWTAuthentication]
    allowed_methods = ['delete']

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
        self.kwargs.update({'clayful': request.META.get('HTTP_CLAYFUL')})
        try:
            clayful_wishlist_client = ClayfulWishListClient(clayful=self.kwargs['clayful'])
            delete_item = clayful_wishlist_client.delete_item(product_id=request.POST['product_id'])
            if not delete_item.status == 204:
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
            else:
                return Response(delete_item.data, status=status.HTTP_200_OK)
        except Exception as errors:
            raise ValidationError({'error_msg': errors.args[0]['delete_item'][0]})
