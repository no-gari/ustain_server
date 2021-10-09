from api.commerce.customer.models import UserShipping
from api.user.models import User
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserShipping
        exclude = ('user',)


class UserPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['points']
