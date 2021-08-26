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
