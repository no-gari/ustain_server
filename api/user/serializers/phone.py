from rest_framework.exceptions import ValidationError
from api.user.models import User, PhoneVerifier
from api.logger.models import PhoneLog
from rest_framework import serializers
from django.utils import timezone
from django.db import transaction
import hashlib
import random


class PasswordChangeVerifierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerifier
        fields = ['phone']

    def validate(self, attrs):
        phone = attrs['phone']
        if not User.objects.filter(phone=phone).exists():
            raise ValidationError({'error_msg': '존재하지 않는 휴대폰입니다.'})
        code = ''.join([str(random.randint(0, 9)) for i in range(6)])
        created = timezone.now()
        hash_string = str(phone) + code + str(created.timestamp())
        token = hashlib.sha1(hash_string.encode('utf-8')).hexdigest()
        attrs.update({'code': code, 'token': token, 'created': created})
        try:
            self.send_code(attrs)
        except Exception:
            raise ValidationError({'error_msg': '인증번호 전송 실패'})
        return attrs

    def send_code(self, attrs):
        body = f'어스테인 비밀번호 찾기 인증번호: [{attrs["code"]}]'
        PhoneLog.objects.create(to=attrs['phone'], body=body)


class PasswordChangeVerifierConfirmSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField(write_only=True)
    phone_token = serializers.CharField(read_only=True, source='token')

    def validate(self, attrs):
        phone = attrs['phone']
        code = attrs['code']
        try:
            phone_verifier = PhoneVerifier.objects.get(phone=phone, code=code)
        except PhoneVerifier.DoesNotExist:
            raise ValidationError({'error_msg': '인증번호가 일치하지 않습니다.'})
        attrs.update({'token': phone_verifier.token})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        return validated_data


class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    phone_token = serializers.CharField(write_only=True)
    phone = serializers.CharField()

    class Meta:
        model = User
        fields = ['password', 'password_confirm', 'phone', 'phone_token']

    def validate(self, attrs):
        password = attrs['password']
        password_confirm = attrs['password_confirm']
        phone = attrs['phone']
        phone_token = attrs['phone_token']
        if password != password_confirm:
            raise ValidationError({'error_msg': '비밀번호가 일치하지 않습니다.'})
        try:
            self.phone_verifier = PhoneVerifier.objects.get(phone=phone, token=phone_token)
        except PhoneVerifier.DoesNotExist:
            raise ValidationError({'error_msg': '휴대폰 인증을 진행해주세요.'})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.get(phone=validated_data['phone'])
        user.set_password(validated_data['password'])
        self.phone_verifier.delete()
        user.save()
        return {'phone': user.phone}
