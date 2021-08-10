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
    like_user_count = serializers.IntegerField(source='like_users.count')
    is_like = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()

    class Meta:
        model = Magazines
        fields = ['categories', 'id', 'title', 'hits', 'created_at', 'updated_at', 'comments_banned',
                  'like_user_count', 'is_like', 'total_comments']

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.like_users.all()
        else:
            return False

    def get_total_comments(self, obj):
        total_comments = obj.magazine_comments.count()
        return total_comments


class MagazineLikeSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = Magazines
        fields = ['is_like']

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.like_users.all()
        else:
            return False

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user in instance.like_users.all():
            instance.like_users.remove(user)
        else:
            instance.like_users.add(user)
        return instance


class MagazineReviewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MagazineComments
        fields = '__all__'


class MagazineReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MagazineComments
        fields = '__all__'
