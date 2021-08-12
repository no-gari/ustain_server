from rest_framework.generics import CreateAPIView

from api.user.serializers.register import *

class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer