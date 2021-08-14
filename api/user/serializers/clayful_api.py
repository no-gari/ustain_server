import hashlib
import random

from django.db import transaction
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from api.logger.models import PhoneLog, EmailLog
from rest_framework.exceptions import ValidationError
from api.user.models import User, EmailVerifier, PhoneVerifier
from clayful import Clayful


class ClayfulRegisterSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        try:
            Customer = Clayful.Customer

            # 데이터 전송시 application/json 컨텐츠 타입을 사용해야합니다.
            payload = {
                # 'userId': 'user_id',
                'email': validated_data.get('email'),
                'password': validated_data.get('password')
            }

            options = {
                'client': settings.CLAYFUL_API_KEY,
                # 'customer': '<customer-auth-token>',
                'language': 'ko',
                'currency': 'KRW',
                'time_zone': 'Asia/Seoul',
                'debug_language': 'ko'
            }

            response = Customer.create(payload, options)

            print(response.data)
            # headers = response.headers
            # data = response.data
            return response.data

        except Exception as e:
            # Error case
            print(e.code)
            raise ValidationError(e.code)