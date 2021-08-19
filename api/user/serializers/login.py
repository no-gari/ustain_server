import jwt
import requests
from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from api.clayful_client import ClayfulCustomerClient
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from api.user.models import User, Social, SocialKindChoices
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer


class UserSocialLoginSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True)
    state = serializers.CharField(write_only=True)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    is_register = serializers.BooleanField(read_only=True)

    def validate(self, attrs):
        code = attrs['code']
        state = attrs['state']

        if state in SocialKindChoices:
            attrs['social_user_id'] = self.get_social_user_id(code, state)
        else:
            raise ValidationError({'kind': '지원하지 않는 소셜 타입입니다.'})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        social_user_id = validated_data['social_user_id']
        state = validated_data['state']
        user, created = User.objects.get_or_create(email=f'{social_user_id}@{state}', defaults={
            'password': make_password(None),
        })

        if created:
            Social.objects.create(user=user, kind=state)

        refresh = RefreshToken.for_user(user)
        return {
            'access': refresh.access_token,
            'refresh': refresh,
        }

    def get_social_user_id(self, code, state):
        social_user_id = getattr(self, f'get_{state}_user_id')(code)
        return social_user_id

    def get_kakao_user_id(self, code):
        url = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.KAKAO_CLIENT_ID,
            'redirect_uri': settings.SOCIAL_REDIRECT_URL,
            'code': code,
            'client_secret': settings.KAKAO_CLIENT_SECRET,
        }
        response = requests.post(url=url, data=data)
        if not response.ok:
            raise ValidationError('KAKAO GET TOKEN API ERROR')
        data = response.json()

        url = 'https://kapi.kakao.com/v2/user/me'
        headers = {
            'Authorization': f'Bearer {data["access_token"]}'
        }
        response = requests.get(url=url, headers=headers)
        if not response.ok:
            raise ValidationError('KAKAO ME API ERROR')
        data = response.json()

        return data['id']

    def get_apple_user_id(self, code):
        url = 'https://appleid.apple.com/auth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.APPLE_CLIENT_ID,
            'client_secret': settings.APPLE_CLIENT_SECRET,
            'redirect_uri': settings.SOCIAL_REDIRECT_URL,
            'code': code,
        }
        response = requests.post(url=url, data=data)
        if not response.ok:
            raise ValidationError('APPLE GET TOKEN API ERROR')
        data = response.json()

        decoded = jwt.decode(data['id_token'], '', verify=False)

        return decoded['sub']


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
        clayful_customer_client = ClayfulCustomerClient()
        clayful_login = clayful_customer_client.clayful_login(email=self.user.email)
        data['clayful'] = clayful_login.data['token']
        return data
