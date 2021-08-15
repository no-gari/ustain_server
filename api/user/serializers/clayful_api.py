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
    email = serializers.CharField(required=True)

    user_id = serializers.CharField(read_only=True)

    def validate(self, attrs):
        try:
            Clayful.config({
                'client': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ImI5ZDM1MjFhNjFhYTQ4OWYwNWY2ZWQwOWVlYjU5ZmFhYWQ2NjdjOGEwYTEwNTRiOTY0YTJkM2E5ZjczM2EyZjgiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjI5MDA3NjA4LCJzdG9yZSI6IjRINlhaTEdUNzU3TS44WVVBWlpTQTRTQUMiLCJzdWIiOiJCSkhMS0tFVkU5WUEifQ.ZZV0TUGuOAekbhipF2jpiiKzFe_Sd19171LgOs4hsCM",
                'debug_language': 'ko'
            })

            customer = Clayful.Customer

            payload = {
                'connect': True,
                'userId': attrs.get('email'),
            }

            response = customer.create(payload)

            attrs.update({
                'user_id': response.data.get('userId')
            })
        except Exception as err:
            raise ValidationError({'code': err.code, 'message': err.message})
        return attrs

    def create(self, validated_data):
        return validated_data


class ClayfulLoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)

    customer = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    expires_in = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        try:
            Customer = Clayful.Customer

            payload = {
                'userId': attrs.get('user_id')
            }

            response = Customer.authenticate(payload)

            attrs.update({
                'customer': response.data.get('customer'),
                'token': response.data.get('token'),
                'expires_in': response.data.get('expiresIn')
            })
        except Exception as err:
            raise ValidationError({'code': err.code, 'message': err.message})
        return attrs

    def create(self, validated_data):
        return validated_data
