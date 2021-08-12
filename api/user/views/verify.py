from rest_framework.generics import CreateAPIView

from api.user.serializers.verify import *


class EmailVerifierCreateView(CreateAPIView):
    serializer_class = EmailVerifierCreateSerializer


class EmailVerifierConfirmView(CreateAPIView):
    serializer_class = EmailVerifierConfirmSerializer


class PhoneVerifierCreateView(CreateAPIView):
    serializer_class = PhoneVerifierCreateSerializer


class PhoneVerifierConfirmView(CreateAPIView):
    serializer_class = PhoneVerifierConfirmSerializer