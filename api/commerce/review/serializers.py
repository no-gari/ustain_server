from rest_framework.validators import ValidationError
from rest_framework import serializers


class ReviewCountSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs


class ReviewListSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs


class ReviewRetrieveSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs


class ReviewCreateSerializer(serializers.Serializer)
    def validate(self, attrs):
        return attrs


class ReviewDeleteSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs
