from rest_framework.validators import ValidationError
from rest_framework import serializers


class QNACountSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs


class QNAListSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs


class QNARetrieveSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs


class QNACreateSerializer(serializers.Serializer)
    def validate(self, attrs):
        return attrs


class QNADeleteSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs
