from rest_framework.generics import CreateAPIView, GenericAPIView


from api.user.serializers.register import *


class PhoneVerifierCreateView(CreateAPIView):
    serializer_class = PhoneVerifierCreateSerializer


class PhoneVerifierConfirmView(CreateAPIView):
    serializer_class = PhoneVerifierConfirmSerializer


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
