from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from api.user.serializers.register import PhoneVerifierCreateSerializer, PhoneVerifierConfirmSerializer, UserRegisterSerializer


class PhoneVerifierCreateView(CreateAPIView):
    serializer_class = PhoneVerifierCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.create(request, *args, **kwargs)
        if serializer.status_code == 201:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return serializer


class PhoneVerifierConfirmView(CreateAPIView):
    serializer_class = PhoneVerifierConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.create(request, *args, **kwargs)
        if serializer.status_code == 201:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return serializer


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.create(request, *args, **kwargs)
        if serializer.status_code == 201:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return serializer
