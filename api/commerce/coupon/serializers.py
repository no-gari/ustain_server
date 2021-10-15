from rest_framework import serializers
from django.utils.html import strip_tags


class CouponSerializer(serializers.Serializer):
    _id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    expires_at = serializers.SerializerMethodField()

    def get_description(self, value):
        description = value.get('description', None)
        return None if description == None else strip_tags(description)

    def get_min_price(self, value):
        try:
            min_price = value['price']['min']['raw']
            return min_price
        except:
            return None

    def get_discount(self, value):
        try:
            discount = value['discount']['value']['raw']
            return discount
        except:
            return None

    def get_expires_at(self, value):
        try:
            expires_at = value['expiresAt']['formatted']
            return expires_at
        except:
            return None


class CouponDetailSerializer(serializers.Serializer):
    _id = serializers.CharField()
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    expires_at = serializers.SerializerMethodField()

    def get_name(self, value):
        try:
            name = value['name']['ko']
            return name
        except:
            return None

    def get_description(self, value):
        try:
            description = strip_tags(value['description']['ko'])
            return description
        except:
            return None

    def get_min_price(self, value):
        try:
            min_price = value['price']['min']
            return min_price
        except:
            return None

    def get_discount(self, value):
        try:
            discount = value['discount']['value']
            return discount
        except:
            return None

    def get_expires_at(self, value):
        return None
