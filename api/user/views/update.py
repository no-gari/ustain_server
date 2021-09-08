from rest_framework import status
from rest_framework.response import Response
from api.clayful_client import ClayfulCustomerClient
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from api.user.serializers.update import UserProfileSerializer, PhoneUpdateVerifierCreateSerializer, PhoneUpdateVerifierConfirmSerializer


class UserProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ['put', 'get', 'delete']

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        clayful = self.request.data['clayful']
        clayful_customer_client = ClayfulCustomerClient()
        clayful_customer_client.clayful_customer_delete(clayful=clayful)
        del_user = self.request.user
        del_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PhoneUpdateVerifierCreateView(CreateAPIView):
    serializer_class = PhoneUpdateVerifierCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class PhoneUpdateVerifierConfirmView(CreateAPIView):
    serializer_class = PhoneUpdateVerifierConfirmSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
