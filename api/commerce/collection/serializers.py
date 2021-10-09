from rest_framework import serializers


class CollectionRetrieveSerializers(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
