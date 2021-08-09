import requests
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class MagazinesListSerializer(serializers.ModelSerializer):
    pass


class MagazineRetrieveSerializer(serializers.ModelSerializer):
    pass


class MagazineLikeUserListSerializer(serializers.ModelSerializer):
    pass


class MagazineLikeCreateSerializer(serializers.ModelSerializer):
    pass


class MagazineLikeDeleteSerializer(serializers.ModelSerializer):
    pass


class MagazineReviewsListSerializer(serializers.ModelSerializer):
    pass


class MagazineReviewSerializer(serializers.ModelSerializer):
    pass