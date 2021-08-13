from rest_framework.generics import CreateAPIView
from api.user.serializers.login import *


class UserSocialLoginView(CreateAPIView):
    serializer_class = UserSocialLoginSerializer