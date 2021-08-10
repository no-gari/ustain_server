import requests
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from .models import Magazines, MagazineComments
from rest_framework.exceptions import ValidationError


class MagazinesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magazines
        fields = '__all__'


class MagazineRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magazines
        fields = '__all__'


class MagazineLikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magazines
        fields = '__all__'


class MagazineLikeDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magazines
        fields = '__all__'


class MagazineReviewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MagazineComments
        fields = '__all__'


class MagazineReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MagazineComments
        fields = '__all__'
