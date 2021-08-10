import hashlib
import random

import jwt
import requests
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api.logger.models import PhoneLog, EmailLog
from api.user.models import User, EmailVerifier, PhoneVerifier, Social, SocialKindChoices
from api.user.validators import validate_password


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, required=False)
    email_token = serializers.CharField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=False)
    phone_token = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    password_confirm = serializers.CharField(write_only=True, required=False)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def get_fields(self):
        fields = super().get_fields()

        if 'email' in User.VERIFY_FIELDS:
            fields['email_token'].required = True
        if 'email' in User.VERIFY_FIELDS or 'email' in User.REGISTER_FIELDS:
            fields['email'].required = True
        if 'phone' in User.VERIFY_FIELDS:
            fields['phone_token'].required = True
        if 'phone' in User.VERIFY_FIELDS or 'phone' in User.REGISTER_FIELDS:
            fields['phone'].required = True
        if 'password' in User.REGISTER_FIELDS:
            fields['password'].required = True
            fields['password_confirm'].required = True

        return fields

    def validate(self, attrs):
        email = attrs.get('email')
        email_token = attrs.pop('email_token', None)
        phone = attrs.get('phone')
        phone_token = attrs.pop('phone_token', None)

        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)

        if 'email' in User.VERIFY_FIELDS:
            # 이메일 토큰 검증
            try:
                self.email_verifier = EmailVerifier.objects.get(email=email, token=email_token)
            except EmailVerifier.DoesNotExist:
                raise ValidationError('이메일 인증을 진행해주세요.')
        if 'email' in User.VERIFY_FIELDS or 'email' in User.REGISTER_FIELDS:
            # 이메일 검증
            if User.objects.filter(email=email).exists():
                raise ValidationError({'email': ['이미 가입된 이메일입니다.']})

        if 'phone' in User.VERIFY_FIELDS:
            # 휴대폰 토큰 검증
            try:
                self.phone_verifier = PhoneVerifier.objects.get(phone=phone, token=phone_token)
            except PhoneVerifier.DoesNotExist:
                raise ValidationError('휴대폰 인증을 진행해주세요.')
        if 'phone' in User.VERIFY_FIELDS or 'phone' in User.REGISTER_FIELDS:
            # 휴대폰 검증
            if User.objects.filter(phone=phone).exists():
                raise ValidationError({'phone': ['이미 가입된 휴대폰입니다.']})

        if 'password' in User.REGISTER_FIELDS:
            errors = {}
            # 비밀번호 검증
            if password != password_confirm:
                errors['password'] = ['비밀번호가 일치하지 않습니다.']
                errors['password_confirm'] = ['비밀번호가 일치하지 않습니다.']
            else:
                try:
                    validate_password(password)
                except DjangoValidationError as error:
                    errors['password'] = list(error)
                    errors['password_confirm'] = list(error)

            if errors:
                raise ValidationError(errors)

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data,
        )
        if 'email' in User.VERIFY_FIELDS:
            self.email_verifier.delete()
        if 'phone' in User.VERIFY_FIELDS:
            self.phone_verifier.delete()

        refresh = RefreshToken.for_user(user)

        return {
            'access': refresh.access_token,
            'refresh': refresh,
        }