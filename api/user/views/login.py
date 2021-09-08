from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.user.serializers.login import *


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
