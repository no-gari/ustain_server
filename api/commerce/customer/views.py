from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from api.commerce.customer.serializers import AddressSerializer
from api.commerce.customer.models import UserShipping
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class AddressListView(ListAPIView):
    model = UserShipping
    serializer_class = AddressSerializer

    def get_queryset(self):
        user_addresses = UserShipping.objects.filter(user=self.request.user)
        return user_addresses

    def list(self, request, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
        return super().list(request, **kwargs)


class AddressView(RetrieveUpdateAPIView):
    queryset = UserShipping.objects.all()
    serializer_class = AddressSerializer
    allowed_methods = ['GET', 'PATCH']
    model = UserShipping
    lookup_field = 'pk'

    def retrieve(self, request, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
        return super().retrieve(self, request, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('is_default') == 'True':
            addresses = UserShipping.objects.filter(user=request.user)
            for address in addresses:
                address.is_default = False
                address.save()
        return super().patch(request, *args, **kwargs)


@api_view(["POST"])
def create_address(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        serializer_data = AddressSerializer(request.data).data
        if serializer_data['is_default'] is True:
            addresses = UserShipping.objects.filter(user=request.user)
            for address in addresses:
                address.is_default = False
                address.save()
        new_user_shipping = UserShipping.objects.create(
            user=request.user,
            name=serializer_data.get('name'),
            big_address=serializer_data.get('big_address'),
            small_address=serializer_data.get('small_address'),
            postal_code=serializer_data.get('postal_code'),
            phone_number=serializer_data.get('phone_number'),
            is_default=serializer_data.get('is_default')
        )
        new_user_shipping.save()
        return Response(AddressSerializer(new_user_shipping).data, status=status.HTTP_200_OK)
    except:
        return ValidationError({'error_msg': '다시 한 번 시도 해주세요.'})


@api_view(["DELETE"])
def delete_address(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        id = int(request.data.get('id'))
        user_shipping = UserShipping.objects.get(id=id)
        user_shipping.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return ValidationError({'error_msg': '다시 한 번 시도 해주세요.'})
