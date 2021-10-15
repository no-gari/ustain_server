from api.commerce.customer.serializers import AddressSerializer
from rest_framework import serializers
from datetime import datetime


class CheckOutSerializer(serializers.Serializer):
    _id = serializers.CharField()
    product = serializers.SerializerMethodField()
    variant = serializers.SerializerMethodField()
    price = serializers.CharField()
    quantity = serializers.CharField()
    addedAt = serializers.SerializerMethodField()

    def get_product(self, value):
        return value['product_id']

    def get_variant(self, value):
        return value['variant_id']

    def get_added_at(self):
        return datetime.now()


class OrderSerializer(serializers.Serializer):
    products = CheckOutSerializer(many=True)
    address = AddressSerializer()
    pay_method = serializers.CharField()
    request = serializers.SerializerMethodField()
