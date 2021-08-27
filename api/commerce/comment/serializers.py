from rest_framework.validators import ValidationError
from rest_framework import serializers


class RetrieveCommentSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs
