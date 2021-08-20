from clayful import Clayful

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.clayful_client import ClayfulProductClient
from api.user.models import Categories


class ProductListByCategoriesSerializer(serializers.Serializer):
    categories = serializers.ListField(required=True)

    products = serializers.JSONField(read_only=True)

    def validate(self, attrs):
        mids = attrs.get('categories')
        for mid in mids:
            try:
                Categories.objects.get(mid=mid)
            except Categories.DoesNotExist:
                raise ValidationError({'categories': ['%s: 존재하지 않는 카테고리입니다.'%mid]})

        # collection 이름에 해당하는 상품 가져오기
        clayful_product_client = ClayfulProductClient()
        list_categories = clayful_product_client.list_categories(collection=','.join(mids))

        if not list_categories.status == 200:
            raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
        else:
            attrs.update({'products': list_categories.data})

        return attrs

    def create(self, validated_data):
        return validated_data

