from api.commerce.customer.models import UserShipping, ShippingRequest
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserShipping
        exclude = ('user',)


class UserPointSerializer(serializers.Serializer):
    used = serializers.CharField()
    available = serializers.CharField()


class ShippingrRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShippingRequest
        fields = '__all__'
