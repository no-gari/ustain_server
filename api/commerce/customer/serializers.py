from api.commerce.customer.models import UserShipping, ShippingRequest
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserShipping
        exclude = ('user',)


class ShippingrRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShippingRequest
        fields = '__all__'
