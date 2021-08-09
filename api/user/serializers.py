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
            'is_register': user.is_register,
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

    def get_naver_user_id(self, code):
        url = 'https://nid.naver.com/oauth2.0/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.NAVER_CLIENT_ID,
            'client_secret': settings.NAVER_CLIENT_SECRET,
            'code': code,
        }
        response = requests.post(url=url, data=data)
        if not response.ok:
            raise ValidationError('NAVER GET TOKEN API ERROR')
        data = response.json()

        url = 'https://openapi.naver.com/v1/nid/me'
        headers = {
            'Authorization': f'Bearer {data["access_token"]}'
        }
        response = requests.post(url=url, headers=headers)
        if not response.ok:
            raise ValidationError('NAVER ME API ERROR')
        data = response.json()

        return data['response']['id']

    def get_facebook_user_id(self, code):
        url = 'https://graph.facebook.com/v9.0/oauth/access_token'
        params = {
            'client_id': settings.FACEBOOK_CLIENT_ID,
            'client_secret': settings.FACEBOOK_CLIENT_SECRET,
            'redirect_uri': settings.SOCIAL_REDIRECT_URL,
            'code': code,
        }
        response = requests.get(url=url, params=params)
        if not response.ok:
            raise ValidationError('FACEBOOK GET TOKEN API ERROR')
        data = response.json()

        url = 'https://graph.facebook.com/debug_token'
        params = {
            'input_token': data['access_token'],
            'access_token': data['access_token'],
        }
        response = requests.get(url=url, params=params)
        if not response.ok:
            raise ValidationError('FACEBOOK ME API ERROR')
        data = response.json()

        return data['data']['user_id']

    def get_google_user_id(self, code):
        url = 'https://oauth2.googleapis.com/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.SOCIAL_REDIRECT_URL,
            'code': code,
        }
        response = requests.post(url=url, data=data)
        if not response.ok:
            raise ValidationError('GOOGLE GET TOKEN API ERROR')
        data = response.json()

        decoded = jwt.decode(data['id_token'], '', verify=False)

        return decoded['sub']

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


class EmailVerifierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerifier
        fields = ['email']

    def validate(self, attrs):
        email = attrs['email']

        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': ['이미 존재하는 이메일입니다.']})

        code = ''.join([str(random.randint(0, 9)) for i in range(6)])
        created = timezone.now()
        hash_string = str(email) + code + str(created.timestamp())
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

        return attrs

    def send_code(self, attrs):
        pass


class EmailVerifierConfirmSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    code = serializers.CharField(write_only=True)
    email_token = serializers.CharField(read_only=True, source='token')

    class Meta:
        model = EmailVerifier
        fields = ['email', 'code', 'email_token']

    def validate(self, attrs):
        email = attrs['email']
        code = attrs['code']
        try:
            email_verifier = self.Meta.model.objects.get(email=email, code=code)
        except self.Meta.model.DoesNotExist:
            raise ValidationError({'code': ['인증번호가 일치하지 않습니다.']})

        attrs.update({'token': email_verifier.token})
        return attrs

    def create(self, validated_data):
        return validated_data


class PhoneVerifierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerifier
        fields = ['phone']

    def validate(self, attrs):
        phone = attrs['phone']

        if User.objects.filter(phone=phone).exists():
            raise ValidationError({'phone': ['이미 존재하는 휴대폰입니다.']})

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

        return attrs

    def send_code(self, attrs):
        body = f'어라운드어스 회원가입 인증번호: [{attrs["code"]}]'
        PhoneLog.objects.create(to=attrs['phone'], body=body)


class PhoneVerifierConfirmSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)
    phone_token = serializers.CharField(read_only=True, source='token')

    class Meta:
        model = PhoneVerifier
        fields = ['phone', 'code', 'phone_token']

    def validate(self, attrs):
        phone = attrs['phone']
        code = attrs['code']
        try:
            phone_verifier = self.Meta.model.objects.get(phone=phone, code=code)
        except self.Meta.model.DoesNotExist:
            raise ValidationError({'code': ['인증번호가 일치하지 않습니다.']})

        attrs.update({'token': phone_verifier.token})
        return attrs

    def create(self, validated_data):
        return validated_data


class EmailFoundPhoneVerifierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerifier
        fields = ['phone']

    def validate(self, attrs):
        phone = attrs['phone']

        if not User.objects.filter(phone=phone).exists():
            raise ValidationError({'phone': ['존재하지 않는 휴대폰입니다.']})

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

        return attrs

    def send_code(self, attrs):
        body = f'어라운드어스 이메일 찾기 인증번호: [{attrs["code"]}]'
        PhoneLog.objects.create(to=attrs['phone'], body=body)


class EmailFoundPhoneVerifierConfirmSerializer(serializers.Serializer):
    '''
    request로 넘어온 phone과 code의 일치 여부 확인 후, 일치할 경우 해당 phone과 일치하는 user의 email 정보를 반환한다.
    '''
    phone = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)
    phone_token = serializers.CharField(read_only=True, source='token')

    email = serializers.EmailField(read_only=True)

    def validate(self, attrs):
        phone = attrs['phone']
        code = attrs['code']
        try:
            phone_verifier = PhoneVerifier.objects.get(phone=phone, code=code)
        except PhoneVerifier.DoesNotExist:
            raise ValidationError({'code': ['인증번호가 일치하지 않습니다.']})

        attrs.update({'token': phone_verifier.token})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        print(**validated_data)
        phone = validated_data.get('phone')
        user = User.objects.get(phone=phone)

        return {
            'email': user.email
        }


class PasswordResetVerifySerializer(serializers.ModelSerializer):
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
        hash_string = str(email) + code + str(created.timestamp())
        token = hashlib.sha1(hash_string.encode('utf-8')).hexdigest()

        attrs.update({
            'code': code,
            'token': token,
            'created': created,
        })

        try:
            self.send_link(attrs)
        except Exception:
            raise ValidationError('비밀번호 재설정 링크 전송 실패')

        return attrs

    def send_link(self, attrs):
        body = f'http://localhost:8000/api/v1/user/password-reset/%s/%s' % (attrs['code'], attrs['token'])
        EmailLog.objects.create(to=attrs['email'], body=body)


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    email_token = serializers.CharField(source='token')
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        email_token = attrs.pop('email_token', None)
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)
        # 이메일 토큰 검증
        try:
            self.email_verifier = EmailVerifier.objects.get(email=email, token=email_token)
        except EmailVerifier.DoesNotExist:
            raise ValidationError('유효한 링크가 아닙니다.')

        # 이메일 검증
        if not User.objects.filter(email=email).exists():
            raise ValidationError({'email': ['존재하지 않는 이메일입니다.']})

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
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        user = User.objects.get(email=email)
        user.password = password
        user.save()

        return user
