from rest_framework import serializers


class ProductListSerializer(serializers.Serializer):
    _id = serializers.CharField()
    name = serializers.CharField()
    hashtags = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    original_price = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    discount_rate = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    def get_hashtags(self, value):
        if value['keywords'] == "":
            return []
        else:
            return value['keywords'].split(' ')

    def get_thumbnail(self, value):
        return value['thumbnail']['url']

    def get_rating(self, value):
        return value['rating']['average']['formatted']

    def get_original_price(self, value):
        return str(value['price']['original']['raw'])

    def get_discount_price(self, value):
        return str(value['price']['sale']['raw'])

    def get_discount_rate(self, value):
        return str(value['discount']['value']['raw'])

    def get_brand(self, value):
        return value['brand']['name']


class ProductDetailSerializer(serializers.Serializer):
    class OptionSerializer(serializers.Serializer):
        _id = serializers.CharField()
        name = serializers.CharField()
        variations = serializers.SerializerMethodField()

        def get_variations(self, value):
            try:
                variations = value['variations']
                for variation in variations:
                    variation.pop('priority')
                return variations
            except:
                return {}

    class VariantSerializer(serializers.Serializer):
        _id = serializers.CharField()
        variant_name = serializers.SerializerMethodField()
        original_price = serializers.SerializerMethodField()
        discount_price = serializers.SerializerMethodField()
        discount_rate = serializers.SerializerMethodField()
        available = serializers.BooleanField()
        thumbnail = serializers.SerializerMethodField()
        types = serializers.SerializerMethodField()

        def get_variant_name(self, value):
            try:
                name_value = ''
                types = value['types']
                for type in types:
                    res_name = "{} : {}".format(type['option']['name'], type['variation']['value'])
                    name_value += res_name
                    if not type == types[-1]:
                        name_value += ' / '
                return name_value
            except:
                return ''

        def get_original_price(self, value):
            try:
                org_price = str(value['price']['original']['raw'])
                return org_price
            except:
                return ''

        def get_discount_price(self, value):
            try:
                dis_price = str(value['price']['sale']['raw'])
                return dis_price
            except:
                return ''

        def get_discount_rate(self, value):
            try:
                dis_rate = str(value['discount']['value']['raw'])
                return dis_rate
            except:
                return ''

        def get_thumbnail(self, value):
            try:
                thumbnail = value['thumbnail']['url']
                return thumbnail
            except:
                return ''

        def get_types(self, value):
            try:
                type_value = {}
                types = value['types']
                for type in types:
                    type_value.update({type['option']['_id']: type['variation']['_id']})
                return types
            except:
                return {}

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
    options = OptionSerializer(required=False, many=True)
    variants = VariantSerializer(required=False, many=True)

    def get_rating(self, value):
        try:
            rating = value['rating']['average']['formatted']
            return rating
        except:
            return ''

    def get_original_price(self, value):
        try:
            org_price = str(value['price']['original']['raw'])
            return org_price
        except:
            return ''

    def get_discount_price(self, value):
        try:
            dis_price = str(value['price']['sale']['raw'])
            return dis_price
        except:
            return ''

    def get_discount_rate(self, value):
        try:
            dis_rate = str(value['discount']['value']['raw'])
            return dis_rate
        except:
            return ''

    def get_brand(self, value):
        try:
            brand = value['brand']
            brand['url'] = value['brand']['logo']['url']
            brand.pop('slug')
            brand.pop('logo')
            return brand
        except:
            return {}

    def get_thumbnail(self, value):
        try:
            thumbnail = value['thumbnail']['url']
            return thumbnail
        except:
            return ''

    def get_total_reviews(self, value):
        try:
            reviews = str(value['totalReview']['raw'])
            return reviews
        except:
            return ''
