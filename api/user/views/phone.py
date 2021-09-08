from api.user.serializers.phone import PasswordChangeVerifierCreateSerializer, PasswordChangeVerifierConfirmSerializer, \
    PasswordChangeSerializer
from rest_framework.generics import CreateAPIView


class PasswordChangeVerifierCreateView(CreateAPIView):
    serializer_class = PasswordChangeVerifierCreateSerializer


class PasswordChangeVerifierConfirmView(CreateAPIView):
    serializer_class = PasswordChangeVerifierConfirmSerializer


class PasswordChangeView(CreateAPIView):
    serializer_class = PasswordChangeSerializer
