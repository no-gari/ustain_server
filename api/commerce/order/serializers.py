from rest_framework import serializers
from django.conf import settings


class OrderSerializer(serializers.Serializer):
    currency = serializers.SerializerMethodField()
    paymentMethod = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    request = serializers.SerializerMethodField()

    def get_currency(self, value):
        return 'KRW'

    def get_paymentMethod(self, value):
        return settings.CLAYFUL_PAYMENT_METHOD

    def get_address(self, value):
        postcode = value['address']['postal_code']
        name = value['address']['name']
        address = value['address']['big_address'].split(' ')
        city = address[0]
        address.pop(0)
        address1 = ' '.join(address)
        address2 = value['address']['small_address']
        mobile = value['address']['phone_number']

        return {
            'shipping': {'name': {'full': name}, 'postcode': postcode, 'country': "KR", 'city': city,
                         'address1': address1, 'address2': address2, 'mobile': mobile},
            'billing': {'name': {'full': name}, 'postcode': postcode, 'country': "KR", 'city': city,
                        'address1': address1, 'address2': address2, 'mobile': mobile}}

    def get_discount(self, value):
        discount = value['coupon']['_id']
        return None if discount is None else {'cart': {'coupon': discount}}

    def get_request(self, value):
        request1 = value['request']['shipping_request']['content']
        request2 = value['request']['additional_request']
        return request1 + ' ' + request2


class QueryOptionSerializer(serializers.Serializer):
    products = serializers.SerializerMethodField()

    def get_products(self, value):
        product_string = ''
        for product in value:
            product_string += product['_id']
            if product == product[-1]:
                product_string += ','
        return product_string


class PaymentSerializer(serializers.Serializer):
    merchant_uid = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()
    buyer_tel = serializers.SerializerMethodField()
    buyer_email = serializers.SerializerMethodField()

    def get_merchant_uid(self, value):
        return value['_id']

    def get_name(self, value):
        return value['_id']

    def get_amount(self, value):
        return value['total']['price']['withTax']

    def get_currency(self, value):
        return value['currency']['base']['code']

    def get_buyer_name(self, value):
        return value['address']['shipping']['name']['full']

    def get_buyer_tel(self, value):
        return value['address']['shipping']['mobile']

    def get_buyer_email(self, value):
        return value['customer']['userId']
