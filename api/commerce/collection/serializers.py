from rest_framework import serializers


class CollectionRetrieveSerializers(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)

    def get_thumbnail(self, value):
        try:
            value = value['thumbnail']['url']
            return value
        except:
            return {}
