from rest_framework.validators import ValidationError
from rest_framework import serializers


class RetrieveCartSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs


class AddToCartSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs


class EmptyCartSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs


class DeleteItemSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs


class CountItemSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs


class CheckOutSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs


class CartListSerializer(serializers.Serializer):
    shippingMethod = serializers.JSONField()
    product = serializers.JSONField()
    variant = serializers.JSONField()
    quantity = serializers.JSONField()
    _id = serializers.CharField()
    bundleItems = serializers.JSONField()
    addedAt = serializers.CharField()
    status = serializers.CharField()
    errors = serializers.JSONField()
    type = serializers.CharField()
    brand = serializers.JSONField()
    collections = serializers.JSONField()
    discounts = serializers.JSONField()
    discounted = serializers.JSONField()
    taxes = serializers.JSONField()
    taxed = serializers.JSONField()
    taxCategory = serializers.JSONField()
    price = serializers.JSONField()
    total = serializers.JSONField()


class CartItemSerializer(serializers.Serializer):
    product = serializers.CharField()
    variant = serializers.CharField()
    quantity = serializers.IntegerField()

    shipping_method = serializers.CharField(read_only=True)
    bundle_items = serializers.JSONField(read_only=True)
    added_at = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)

    def create(self, validated_data):
        return validated_data
