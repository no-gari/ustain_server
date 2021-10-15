import random
import hashlib
import datetime
from rest_framework import serializers
from api.logger.models import PhoneLog
from api.user.models import User, PhoneVerifier
from rest_framework.exceptions import ValidationError


class UserProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(read_only=True)
    groups = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['groups', 'phone', 'name', 'profile_article', 'sex_choices', 'birthday', 'categories']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.profile_article = validated_data.get('profile_article', instance.profile_article)
        instance.birthday = validated_data.get('birthday', instance.profile_article)
        sex_choices = validated_data.get('sex_choices')
        if sex_choices == 'MA':
            instance.sex_choices = User.SexChoices.MALE
        else:
            instance.sex_choices = User.SexChoices.FEMALE
        instance.categories.set(validated_data.get('categories', instance.categories))
        instance.save()
        return instance


class PhoneUpdateVerifierCreateSerializer(serializers.Serializer):
    old_phone = serializers.CharField(max_length=11)
    new_phone = serializers.CharField(max_length=11)

    def validate(self, attrs):
        old_phone = attrs['old_phone']
        new_phone = attrs['new_phone']
        if User.objects.filter(phone=new_phone).exists():
            raise ValidationError({'error_msg': '이미 존재하는 핸드폰입니다.'})
        if old_phone == new_phone:
            raise ValidationError({'error_msg': '기존의 번호와 동일합니다.'})
        code = ''.join([str(random.randint(0, 9)) for i in range(6)])
        created = datetime.datetime.now()
        hash_string = str(new_phone) + code + str(created.timestamp())
        token = hashlib.sha1(hash_string.encode('utf-8')).hexdigest()
        attrs.update({'code': code, 'token': token, 'created': created})
        try:
            self.send_code(attrs)
        except Exception:
            raise ValidationError('인증번호 전송 실패')
        new_phone_verifier = PhoneVerifier.objects.create(phone=new_phone, code=code, created=created, token=token)
        new_phone_verifier.save()
        try:
            self.send_code(attrs)
        except Exception:
            raise ValidationError({'error_msg': '인증 번호 전송에 실패하였습니다.'})
        return attrs

    def send_code(self, attrs):
        body = f'어라운드어스 휴대폰 번호 변경 인증번호: [{attrs["code"]}]'
        PhoneLog.objects.create(to=attrs['new_phone'], body=body)

    def create(self, validated_data):
        return validated_data


class PhoneUpdateVerifierConfirmSerializer(serializers.Serializer):
    old_phone = serializers.CharField(write_only=True)
    new_phone = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone = attrs['new_phone']
        code = attrs['code']
        try:
            phone_verifier = PhoneVerifier.objects.get(phone=phone, code=code)
        except PhoneVerifier.DoesNotExist:
            raise ValidationError({'error_msg': '인증번호가 일치하지 않습니다.'})
        phone_verifier.delete()
        return attrs

    def create(self, validated_data):
        old_phone = validated_data.get('old_phone')
        new_phone = validated_data.get('new_phone')
        user = User.objects.get(phone=old_phone)
        user.phone = new_phone
        user.save()
        return validated_data
