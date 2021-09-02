from api.commerce.product.serializers import ProductListSerializer
from api.magazine.serializers import MagazinesListSerializer
from api.clayful_client import ClayfulProductClient
from api.magazine.models import Magazines
from rest_framework import serializers


class BrandRetrieveSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    logo = serializers.SerializerMethodField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)
    createdAt = serializers.SerializerMethodField(read_only=True)
    updatedAt = serializers.SerializerMethodField(read_only=True)
    magazines = serializers.SerializerMethodField(required=False)
    products = serializers.SerializerMethodField(required=False)

    def get_logo(self, value):
        return value['logo']['url']

    def get_thumbnail(self, value):
        return value['thumbnail']['url']

    def get_createdAt(self, value):
        return value['createdAt']['raw']

    def get_updatedAt(self, value):
        return value['updatedAt']['raw']

    def get_magazines(self, value):
        magazines = Magazines.objects.filter(brand=value['_id'])
        magazine_data = MagazinesListSerializer(magazines, many=True).data
        return magazine_data

    def get_products(self, value):
        clayful_product_client = ClayfulProductClient()
        products = clayful_product_client.get_related_products(brand_id=value['_id'])
        product_data = ProductListSerializer(products.data, many=True).data
        return product_data
