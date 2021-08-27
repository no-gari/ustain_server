from rest_framework.validators import ValidationError
from rest_framework import serializers


class UrlSerializer(serializers.Serializer):
    url = serializers.URLField(read_only=True)


class DateTimeSeirializer(serializers.Serializer):
    raw = serializers.DateTimeField(read_only=True)


class BrandRetrieveSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    logo = UrlSerializer(read_only=True)
    thumbnail = UrlSerializer(read_only=True)
    createdAt = DateTimeSeirializer(read_only=True)
    updatedAt = DateTimeSeirializer(read_only=True)
