from rest_framework import serializers


class CollectionRetrieveSerializers(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)

    def get_thumbnail(self, value):
        return value['thumbnail']['url']

#
# class SmallCollectionRetrieveSerializers(serializers.Serializer):
#     _id = serializers.CharField(read_only=True)
#     description = serializers.CharField(read_only=True)
#     name = serializers.CharField(read_only=True)
#     thumbnail = serializers.SerializerMethodField(read_only=True)
#     big_collection = serializers.SerializerMethodField()
#
#     def get_thumbnail(self, value):
#         return value['thumbnail']['url']
#
#     def get_big_collection(self, value):
#         clayful_collection_client = ClayfulCollectionClient()
#         data = CollectionRetrieveSerializers(clayful_collection_client.get_collection(parent=value['parent']['_id']).data).data
#         return data