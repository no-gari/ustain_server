from rest_framework import serializers
from django.conf import settings
from datetime import datetime


class OrderTempSerializer(serializers.Serializer):
    products = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField(read_only=True)
    request = serializers.SerializerMethodField(read_only=True)
    coupon = serializers.SerializerMethodField(read_only=True)
    agreed = serializers.BooleanField(read_only=True)

    def get_products(self, value):
        return value

    def get_payment_method(self, value):
        return settings.CLAYFUL_PAYMENT_METHOD

    def get_agreed(self, value):
        return False


class InstantOrderSerializer(serializers.Serializer):
    currency = serializers.CharField()
    paymentMethod = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    request = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    class AddressSerializer(serializers.Serializer):
        pass



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
#
#
# class OrderSerializer(serializers.Serializer):
#     products = CheckOutSerializer(many=True)
#     address = AddressSerializer()
#     pay_method = serializers.CharField()
#     request = serializers.SerializerMethodField()
