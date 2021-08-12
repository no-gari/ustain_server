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
from api.user.models import User, Categories
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
