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
    magazines = serializers.SerializerMethodField(required=False)
    products = serializers.SerializerMethodField(required=False)

    def get_logo(self, value):
        return value['logo']['url']

    def get_magazines(self, value):
        try:
            magazines = Magazines.objects.filter(brand=value['_id'])
            magazine_data = MagazinesListSerializer(magazines, many=True).data
            return magazine_data
        except:
            return []

    def get_products(self, value):
        clayful_product_client = ClayfulProductClient()
        try:
            products = clayful_product_client.get_related_products(brand_id=value['_id'])
            product_data = ProductListSerializer(products.data, many=True).data
            return product_data[:4]
        except:
            return []
