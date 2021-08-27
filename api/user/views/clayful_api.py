from rest_framework.generics import CreateAPIView

from api.user.serializers.clayful_api import ClayfulRegisterSerializer, ClayfulLoginSerializer


class ClayfulRegisterView(CreateAPIView):
    serializer_class = ClayfulRegisterSerializer


class ClayfulLoginView(CreateAPIView):
    serializer_class = ClayfulLoginSerializer
