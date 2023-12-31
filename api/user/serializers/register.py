import hashlib
import random
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from api.logger.models import PhoneLog
from api.user.models import User, PhoneVerifier
from api.clayful_client import ClayfulCustomerClient
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken


class PhoneVerifierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerifier
        fields = ['phone']

    def validate(self, attrs):
        phone = attrs['phone']

        if User.objects.filter(phone=phone).exists():
            raise ValidationError({'error_msg': '이미 존재하는 휴대폰입니다.'})

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
            raise ValidationError({'error_msg': '인증번호 전송 실패'})

        return attrs

    def send_code(self, attrs):
        body = f'어스테인 회원가입 인증번호: [{attrs["code"]}]'
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
            raise ValidationError({'error_msg': '인증번호가 일치하지 않습니다.'})

        attrs.update({'token': phone_verifier.token})
        return attrs

    def create(self, validated_data):
        return validated_data


class UserRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(write_only=True, required=False)
    phone_token = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    password_confirm = serializers.CharField(write_only=True, required=False)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    clayful = serializers.CharField(read_only=True)

    def get_fields(self):
        fields = super().get_fields()
        if 'phone' in User.VERIFY_FIELDS:
            fields['phone_token'].required = True
        if 'phone' in User.VERIFY_FIELDS or 'phone' in User.REGISTER_FIELDS:
            fields['phone'].required = True
        if 'password' in User.REGISTER_FIELDS:
            fields['password'].required = True
            fields['password_confirm'].required = True

        return fields

    def validate(self, attrs):
        phone = attrs.get('phone')
        phone_token = attrs.pop('phone_token', None)
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)

        if 'phone' in User.VERIFY_FIELDS:
            try:
                self.phone_verifier = PhoneVerifier.objects.get(phone=phone, token=phone_token)
            except PhoneVerifier.DoesNotExist:
                raise ValidationError({'error_msg': '휴대폰 인증을 진행해주세요.'})
        if 'phone' in User.VERIFY_FIELDS or 'phone' in User.REGISTER_FIELDS:
            if User.objects.filter(phone=phone).exists():
                raise ValidationError({'error_msg': '이미 가입된 휴대폰입니다.'})

        if 'password' in User.REGISTER_FIELDS and password != password_confirm:
            raise ValidationError({'error_msg': '비밀번호가 일치하지 않습니다.'})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data,)
        userId = str(user.phone)+'@email.com'
        user.email = userId
        user.points = 1000
        user.save()
        clayful_customer_client = ClayfulCustomerClient()
        clayful_register = clayful_customer_client.clayful_register(email=userId, mobile=str(user.phone))

        if not clayful_register.status == 201:
            user.delete()
            raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
        else:
            if 'phone' in User.VERIFY_FIELDS:
                self.phone_verifier.delete()

            clayful_login = clayful_customer_client.clayful_login(email=userId)
            token = clayful_login.data['token']
            refresh = RefreshToken.for_user(user)

        return {
            'access': refresh.access_token,
            'refresh': refresh,
            'clayful': token
        }
