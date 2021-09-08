from clayful import Clayful
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class ClayfulRegisterSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    user_id = serializers.CharField(read_only=True)

    def validate(self, attrs):
        try:
            Clayful.config({'client': settings.CLAYFUL_BACKEND_TOKEN, 'debug_language': 'ko'})
            customer = Clayful.Customer
            payload = {'connect': True, 'userId': attrs.get('email')}
            response = customer.create(payload)
            attrs.update({'user_id': response.data.get('userId')})
        except Exception as err:
            raise ValidationError({'code': err.code, 'message': err.message})
        return attrs

    def create(self, validated_data):
        return validated_data


class ClayfulLoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    customer = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    expires_in = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        try:
            Customer = Clayful.Customer
            payload = {'userId': attrs.get('user_id')}
            response = Customer.authenticate(payload)
            attrs.update({
                'customer': response.data.get('customer'),
                'token': response.data.get('token'),
                'expires_in': response.data.get('expiresIn')
            })
        except Exception as err:
            raise ValidationError({'code': err.code, 'message': err.message})
        return attrs

    def create(self, validated_data):
        return validated_data
