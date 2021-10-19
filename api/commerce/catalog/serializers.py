from django.utils.html import strip_tags
from rest_framework import serializers


class CatalogListSerializer(serializers.Serializer):
    pass


class CatalogDetailSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.SerializerMethodField()

    def get_description(self, value):
        return None if value['description'] is None else strip_tags(value['description'])
