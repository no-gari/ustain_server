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
    variant_options = serializers.SerializerMethodField()
    # original_price = serializers.SerializerMethodField()
    sale_price = serializers.SerializerMethodField()
    # discount_price = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    # total_original_price = serializers.SerializerMethodField()
    # total_discount_price = serializers.SerializerMethodField()
    # total_sale_price = serializers.SerializerMethodField()

    def get_brand(self, value):
        return value['brand']['name']

    def get_product_id(self, value):
        return value['product']['_id']

    def get_product_name(self, value):
        return value['product']['name']

    def get_product_thumbnail(self, value):
        return value['product']['thumbnail']['url']

    def get_variant_id(self, value):
        return value['variant']['_id']

    def get_variant_options(self, value):
        options = value['variant']['types']
        option_string = '옵션 ('
        for option in options:
            if options[-1] is not option and len(options) is not 1:
                option_string = option_string + option['option']['name'] + ' : ' + option['variation']['value'] + ', '
            else:
                option_string = option_string + option['option']['name'] + ' : ' + option['variation']['value'] + ')'
        return option_string

    # def get_original_price(self, value):
    #     return value['variant']['price']['original']['formatted']

    def get_sale_price(self, value):
        return value['variant']['price']['sale']['formatted']

    # def get_discount_price(self, value):
    #     return value['variant']['discount']['discounted']['formatted']

    def get_quantity(self, value):
        return value['quantity']['formatted']
    #
    # def get_total_orignal_price(self, value):
    #     return value['']
    #
    # def get_total_discount_price(self, value):
    #
    # def get_total_sale_price(self, value):


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
