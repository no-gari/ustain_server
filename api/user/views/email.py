from rest_framework.generics import CreateAPIView

from api.user.serializers.email import *


class EmailVerifierCreateView(CreateAPIView):
    serializer_class = EmailVerifierCreateSerializer


class EmailVerifierConfirmView(CreateAPIView):
    serializer_class = EmailVerifierConfirmSerializer


class EmailFoundPhoneVerifierCreateView(CreateAPIView):
    serializer_class = EmailFoundPhoneVerifierCreateSerializer


class EmailFoundPhoneVerifierConfirmView(CreateAPIView):
    serializer_class = EmailFoundPhoneVerifierConfirmSerializer
