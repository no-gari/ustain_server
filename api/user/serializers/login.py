from api.user.models import User
from api.clayful_client import ClayfulCustomerClient
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer


class CustomJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append({'token_class': AuthToken.__name__,
                                 'token_type': AuthToken.token_type,
                                 'message': e.args[0]})
        raise InvalidToken({'error_msg': '유효하지 않은 토큰입니다.'})


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        clayful_customer_client = ClayfulCustomerClient()
        clayful_login = clayful_customer_client.clayful_login(email=self.user.email)
        data['clayful'] = clayful_login.data['token']
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        get_user = TokenBackend(algorithm='HS256').decode(data['access'], verify=False)
        clayful_customer_client = ClayfulCustomerClient()
        current_user = User.objects.get(id=get_user['user_id'])
        clayful_login = clayful_customer_client.clayful_login(email=current_user.email)
        data['clayful'] = clayful_login.data['token']
        return data
