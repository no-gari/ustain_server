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
        return value['rating']['average']['raw']

    def get_original_price(self, value):
        return value['price']['original']['raw']

    def get_discount_price(self, value):
        return value['price']['sale']['raw']

    def get_discount_rate(self, value):
        return value['discount']['value']['raw']

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
        types = serializers.JSONField()
        # types = serializers.SerializerMethodField()

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
                return None

        def get_original_price(self, value):
            try:
                org_price = value['price']['original']['raw']
                return org_price
            except:
                return None

        def get_discount_price(self, value):
            try:
                dis_price = value['price']['sale']['raw']
                return dis_price
            except:
                return ''

        def get_discount_rate(self, value):
            try:
                dis_rate = value['discount']['value']['raw']
                return dis_rate
            except:
                return None

        def get_thumbnail(self, value):
            try:
                thumbnail = value['thumbnail']['url']
                return thumbnail
            except:
                return None

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
            rating = value['rating']['average']['raw']
            return rating
        except:
            return None

    def get_original_price(self, value):
        try:
            org_price = value['price']['original']['raw']
            return org_price
        except:
            return None

    def get_discount_price(self, value):
        try:
            dis_price = value['price']['sale']['raw']
            return dis_price
        except:
            return None

    def get_discount_rate(self, value):
        try:
            dis_rate = value['discount']['value']['raw']
            return dis_rate
        except:
            return None

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
            return None

    def get_total_reviews(self, value):
        try:
            reviews = value['totalReview']['raw']
            return reviews
        except:
            return None


class ProductCheckoutSerializer(serializers.Serializer):
    brand = serializers.SerializerMethodField()
    _id = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_thumbnail = serializers.SerializerMethodField()
    variant_id = serializers.SerializerMethodField()
    variant_name = serializers.SerializerMethodField()
    sale_price = serializers.SerializerMethodField()
    quantity = serializers.CharField()

    def get__id(self, value):
        return None

    def get_brand(self, value):
        try:
            name = value['products']['brand']['name']
            return name
        except:
            return None

    def get_product_id(self, value):
        try:
            product_id = value['products']['_id']
            return product_id
        except:
            return None

    def get_product_name(self, value):
        try:
            product_name = value['products']['name']
            return product_name
        except:
            return None

    def get_product_thumbnail(self, value):
        try:
            product_thumbnail = value['products']['thumbnail']['url']
            return product_thumbnail
        except:
            return None

    def get_variant_id(self, value):
        try:
            variant_id = value['variant']
            return variant_id
        except:
            return None

    def get_variant_name(self, value):
        variant_id = value['variant']
        options = []
        for variant in value['products']['variants']:
            if variant_id == variant['_id']:
                options = variant['types']
        option_string = '옵션 ('
        for option in options:
            if options[-1] is not option and len(options) != 1:
                option_string = option_string + option['option']['name'] + ' : ' + option['variation']['value'] + ', '
            else:
                option_string = option_string + option['option']['name'] + ' : ' + option['variation']['value'] + ')'
        return option_string

    def get_sale_price(self, value):
        variant_id = value['variant']
        sale_price = 0
        for variant in value['products']['variants']:
            if variant_id == variant['_id']:
                sale_price = variant['price']['sale']['raw']
        return sale_price
