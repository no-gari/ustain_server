from django.utils.html import strip_tags
from rest_framework import serializers


class CatalogSortSerilaizer(serializers.Serializer):
    _id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.SerializerMethodField()

    def get_description(self, value):
        description = value.get('description', None)
        return None if description == None else strip_tags(description)


class CatalogListSerializer(serializers.Serializer):
    pass


class CatalogDetailSerializer(serializers.Serializer):
    pass