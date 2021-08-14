from rest_framework.generics import CreateAPIView

from api.user.serializers.clayful_api import *


class ClayfulRegisterView(CreateAPIView):
    serializer_class = ClayfulRegisterSerializer