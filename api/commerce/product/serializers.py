from rest_framework import serializers


class ProductListSerializer(serializers.Serializer):
    _id = serializers.CharField()
    name = serializers.CharField()
    summary = serializers.CharField()
    description = serializers.CharField()
    rating = serializers.SerializerMethodField()
    original_price = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    discount_rate = serializers.SerializerMethodField()

    def get_rating(self, value):
        return value['rating']['average']['formatted']

    def get_original_price(self, value):
        return value['price']['original']['formatted']

    def get_discount_price(self, value):
        return value['price']['sale']['formatted']

    def get_discount_rate(self, value):
        return value['discount']['value']['formatted']

    def get_max_index(self, value):
        pass


class ProductDetailSerializer(serializers.Serializer):
    _id = serializers.CharField()
    name = serializers.CharField()
    keywords = serializers.CharField()
    summary = serializers.CharField()
    description = serializers.CharField()
    rating = serializers.SerializerMethodField()
    original_price = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    discount_rate = serializers.SerializerMethodField()
    available = serializers.BooleanField()
    brand = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    # options = OptionSerializer(required=False, many=True)
    social_values = serializers.SerializerMethodField()

    def get_rating(self, value):
        return value['rating']['average']['formatted']

    def get_original_price(self, value):
        return value['price']['original']['formatted']

    def get_discount_price(self, value):
        return value['price']['sale']['formatted']

    def get_discount_rate(self, value):
        return value['discount']['value']['formatted']

    def get_brand(self, value):
        brand = value['brand']
        brand['url'] = value['brand']['logo']['url']
        brand.pop('slug')
        brand.pop('logo')
        return brand

    def get_thumbnail(self, value):
        return value['thumbnail']['url']

    def get_total_reviews(self, value):
        return value['totalReview']['formatted']

    def get_social_values(self, value):
        return value['meta']['socialValues']
