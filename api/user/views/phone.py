from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from api.user.serializers.phone import PasswordChangeVerifierCreateSerializer, PasswordChangeVerifierConfirmSerializer, PasswordChangeSerializer


class PasswordChangeVerifierCreateView(CreateAPIView):
    serializer_class = PasswordChangeVerifierCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.create(request, *args, **kwargs)
        if serializer.status_code == 201:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return serializer


class PasswordChangeVerifierConfirmView(CreateAPIView):
    serializer_class = PasswordChangeVerifierConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.create(request, *args, **kwargs)
        if serializer.status_code == 201:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return serializer


class PasswordChangeView(CreateAPIView):
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.create(request, *args, **kwargs)
        if serializer.status_code == 201:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return serializer
