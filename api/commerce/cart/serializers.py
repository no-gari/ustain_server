from rest_framework.validators import ValidationError
from rest_framework import serializers


class EmptyCartSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs


class CountItemSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs


class CheckOutSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs


class CartListSerializer(serializers.Serializer):
    brand = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_thumbnail = serializers.SerializerMethodField()
    variant_id = serializers.SerializerMethodField()
    variant_name = serializers.SerializerMethodField()
    sale_price = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()

    def get_brand(self, value):
        try:
            name = value['brand']['name']
            return name
        except:
            return None

    def get_product_id(self, value):
        try:
            product_id = value['product']['_id']
            return product_id
        except:
            return None

    def get_product_name(self, value):
        try:
            product_name = value['product']['name']
            return product_name
        except:
            return None

    def get_product_thumbnail(self, value):
        try:
            product_thumbnail = value['product']['thumbnail']['url']
            return product_thumbnail
        except:
            return None

    def get_variant_id(self, value):
        try:
            variant_id = value['variant']['_id']
            return variant_id
        except:
            return None

    def get_variant_name(self, value):
        options = value['variant']['types']
        option_string = '옵션 ('
        for option in options:
            if options[-1] is not option and len(options) is not 1:
                option_string = option_string + option['option']['name'] + ' : ' + option['variation']['value'] + ', '
            else:
                option_string = option_string + option['option']['name'] + ' : ' + option['variation']['value'] + ')'
        return option_string

    def get_sale_price(self, value):
        try:
            sale_price = value['variant']['price']['sale']['raw']
            return sale_price
        except:
            return None

    def get_quantity(self, value):
        try:
            quantity = value['quantity']['raw']
            return quantity
        except:
            return None


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
