from rest_framework.validators import ValidationError
from rest_framework import serializers


class BrandRetrieveSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    logo = serializers.SerializerMethodField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)
    createdAt = serializers.SerializerMethodField(read_only=True)
    updatedAt = serializers.SerializerMethodField(read_only=True)

    def get_logo(self, value):
        return value['logo']['url']

    def get_thumbnail(self, value):
        return value['thumbnail']['url']

    def get_createdAt(self, value):
        return value['createdAt']['raw']

    def get_updatedAt(self, value):
        return value['updatedAt']['raw']
