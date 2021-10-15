from rest_framework import status
from rest_framework.response import Response
from api.clayful_client import ClayfulCustomerClient
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from api.user.serializers.update import UserProfileSerializer, PhoneUpdateVerifierCreateSerializer, PhoneUpdateVerifierConfirmSerializer


class UserProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ['put', 'get', 'delete']

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        try:
            clayful = self.request.META['HTTP_CLAYFUL']
            clayful_customer_client = ClayfulCustomerClient()
            response = clayful_customer_client.clayful_customer_delete(clayful=clayful)
            if response.status == 204:
                del_user = self.request.user
                del_user.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            raise ValidationError({'error_msg': '회원 삭제에 실패했습니다.'})


class PhoneUpdateVerifierCreateView(CreateAPIView):
    serializer_class = PhoneUpdateVerifierCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.create(request, *args, **kwargs)
        if serializer.status_code == 201:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return serializer


class PhoneUpdateVerifierConfirmView(CreateAPIView):
    serializer_class = PhoneUpdateVerifierConfirmSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.create(request, *args, **kwargs)
        if serializer.status_code == 201:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return serializer
