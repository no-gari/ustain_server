from api.user.serializers.phone import PasswordChangeVerifierCreateSerializer, PasswordChangeVerifierConfirmSerializer
from rest_framework.generics import CreateAPIView


class PasswordChangeVerifierCreateView(CreateAPIView):
    serializer_class = PasswordChangeVerifierCreateSerializer


class PasswordChangeVerifierConfirmView(CreateAPIView):
    serializer_class = PasswordChangeVerifierConfirmSerializer
