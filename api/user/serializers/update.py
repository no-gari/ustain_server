import random
import hashlib
import datetime
from rest_framework import serializers
from api.logger.models import PhoneLog
from api.user.validators import validate_password
from rest_framework.exceptions import ValidationError
from api.user.tokens import EmailVerificationTokenGenerator
from api.user.models import User, PhoneVerifier


class UserProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    groups = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['groups', 'phone', 'email', 'name', 'profile_article', 'sex_choices', 'birthday', 'categories']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.profile_article = validated_data.get('profile_article', instance.profile_article)
        instance.birthday = validated_data.get('birthday', instance.profile_article)

        # user sex_choices update
        sex_choices = validated_data.get('sex_choices')
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
        created = datetime.datetime.now()
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
