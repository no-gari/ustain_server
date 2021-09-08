from api.user.models import User
from api.clayful_client import ClayfulCustomerClient
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer


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
