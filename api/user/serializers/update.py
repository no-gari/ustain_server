import hashlib
import random
import datetime

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
from api.user.models import User, EmailVerifier, PhoneVerifier
from api.user.tokens import EmailVerificationTokenGenerator
from api.user.validators import validate_password


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['name', 'profile_article', 'sex_choices', 'birthday', 'categories']

    def validate(self, attrs):
        sex_choices = attrs['sex_choices']

        # sex_choices 유효성 검사
        if not (sex_choices == 'MA' or sex_choices == 'FE'):
            raise ValidationError({'sex_choices': ['유효하지 않은 성별입니다.']})

        return attrs

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.profile_article = validated_data.get('profile_article', instance.profile_article)
        instance.birthday = validated_data.get('birthday', instance.profile_article)

        # user sex_choices update
        sex_choices = validated_data.get('sex_choice')
        if sex_choices == 'MA':
            instance.sex_choices = User.SexChoices.MALE
        else:
            instance.sex_choices = User.SexChoices.FEMALE

        # user categories update
        instance.categories.set(validated_data.get('categories', instance.categories))
        instance.save()

        return instance


class PhoneUpdateVerifierCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=11)

    def validate(self, attrs):
        email = attrs['email']
        phone = attrs['phone']

        # find user
        if not User.objects.filter(email=email).exists():
            raise ValidationError({'email': ['존재하지 않는 이메일입니다.']})

        user = User.objects.get(email=email)

        # verified email 인지 확인
        if not user.email_verify:
            raise ValidationError({'email_verify': ['인증되지 않은 이메일입니다.']})

        # 새로운 phone이 맞는지 확인
        if user.phone == phone:
            raise ValidationError({'phone': ['기존의 번호와 동일합니다.']})

        code = ''.join([str(random.randint(0, 9)) for i in range(6)])
        created = timezone.now()
        hash_string = str(phone) + code + str(created.timestamp())
        token = hashlib.sha1(hash_string.encode('utf-8')).hexdigest()

        attrs.update({
            'code': code,
            'token': token,
            'created': created,
        })

        try:
            self.send_code(attrs)
        except Exception:
            raise ValidationError('인증번호 전송 실패')

        PhoneVerifier(phone=phone, code=code, created=created, token=token).save()

        return attrs

    def send_code(self, attrs):
        body = f'어라운드어스 휴대폰 번호 변경 인증번호: [{attrs["code"]}]'
        PhoneLog.objects.create(to=attrs['phone'], body=body, title='어라운드어스 휴대폰 번호 변경 인증번호')

    def create(self, validated_data):
        return validated_data


class PhoneUpdateVerifierConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    phone = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)
    phone_token = serializers.CharField(read_only=True, source='token')

    def validate(self, attrs):
        email = attrs['email']
        phone = attrs['phone']
        code = attrs['code']

        # find user
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError({'email': ['존재하지 않는 이메일입니다.']})

        try:
            phone_verifier = PhoneVerifier.objects.get(phone=phone, code=code)
        except PhoneVerifier.DoesNotExist:
            raise ValidationError({'code': ['인증번호가 일치하지 않습니다.']})

        attrs.update({'token': phone_verifier.token})
        return attrs

    def create(self, validated_data):
        phone = validated_data.get('phone')
        email = validated_data.get('email')

        user = User.objects.get(email=email)
        user.phone = phone
        user.save()

        return validated_data


class PasswordResetVerifierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerifier
        fields = ['email']

    def validate(self, attrs):
        email = attrs['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError({'email': ['존재하지 않는 이메일입니다.']})

        if not user.email_verify:
            raise ValidationError({'email_verify': ['인증되지 않은 이메일입니다.']})

        code = ''.join([str(random.randint(0, 9)) for i in range(6)])
        created = timezone.now()
        token = EmailVerificationTokenGenerator().make_token(user)

        attrs.update({
            'code': code,
            'token': token,
            'created': created,
        })

        try:
            self.send_simple_message(attrs)
        except Exception:
            raise ValidationError('비밀번호 재설정 링크 전송 실패')

        return attrs

    def send_simple_message(self, attrs):
        body = f'http://localhost:8000/api/v1/user/password-reset/%s/%s' % (attrs['code'], attrs['token'])
        EmailLog.objects.create(to=attrs['email'], body=body, title="어라운드어스 비밀번호 재설정 링크")


class PasswordResetSerializer(serializers.Serializer):
    pass


class PasswordResetConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True)
    email_token = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        code = attrs.get('code')
        email_token = attrs.pop('email_token', None)
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)
        # 이메일 토큰 검증
        try:
            self.email_verifier = EmailVerifier.objects.get(code=code, token=email_token)
        except EmailVerifier.DoesNotExist:
            raise ValidationError('유효한 링크가 아닙니다.')

        # 이메일 검증
        if not User.objects.filter(email=self.email_verifier.email).exists():
            raise ValidationError({'email': ['존재하지 않는 이메일입니다.']})
        self.email = self.email_verifier.email

        # password 검증
        errors = {}
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
        password = validated_data.pop('password')

        user = User.objects.get(email=self.email)
        user.set_password(password)
        user.save()

        return user
