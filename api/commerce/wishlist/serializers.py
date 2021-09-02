from rest_framework import serializers


class GetWishListProductsSerializer(serializers.Serializer):
    _id = serializers.CharField()
    name = serializers.CharField()
    summary = serializers.CharField()
    description = serializers.CharField()
    price = serializers.JSONField()
    discount = serializers.JSONField()
    collections = serializers.JSONField()
