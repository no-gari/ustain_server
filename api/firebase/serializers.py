from rest_framework import serializers
from .models import PushToken


class PushTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushToken
        fields = (
            'id',
            'token',
            'user',
        )

