from rest_framework.generics import CreateAPIView

from api.user.serializers import UserRegisterSerializer, EmailVerifierCreateSerializer, \
    PhoneVerifierCreateSerializer, EmailVerifierConfirmSerializer, PhoneVerifierConfirmSerializer, \
    UserSocialLoginSerializer


class UserSocialLoginView(CreateAPIView):
    serializer_class = UserSocialLoginSerializer


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer


class EmailVerifierCreateView(CreateAPIView):
    serializer_class = EmailVerifierCreateSerializer


class EmailVerifierConfirmView(CreateAPIView):
    serializer_class = EmailVerifierConfirmSerializer


class PhoneVerifierCreateView(CreateAPIView):
    serializer_class = PhoneVerifierCreateSerializer


class PhoneVerifierConfirmView(CreateAPIView):
    serializer_class = PhoneVerifierConfirmSerializer

