from api.commerce.customer.models import UserShipping
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserShipping
        exclude = ('user',)
