from api.magazine.models import Magazines, MagazineComments
from rest_framework import serializers


class MagazinesListSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = Magazines
        fields = ['categories', 'banner_image', 'id', 'content', 'title', 'is_like']

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.like_users.all()
        else:
            return False


class MagazineRetrieveSerializer(serializers.ModelSerializer):
    like_user_count = serializers.IntegerField(source='like_users.count')
    is_like = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()

    class Meta:
        model = Magazines
        fields = ['categories', 'banner_image', 'id', 'content', 'title', 'hits', 'created_at', 'updated_at', 'comments_banned',
                  'like_user_count', 'is_like', 'total_comments']

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.like_users.all()
        else:
            return False

    def get_total_comments(self, obj):
        total_comments = obj.magazine_comments.count()
        return total_comments


class MagazineLikeSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = Magazines
        fields = ['is_like']

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.like_users.all()
        else:
            return False

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user in instance.like_users.all():
            instance.like_users.remove(user)
        else:
            instance.like_users.add(user)
        return instance


class MagazineScrapCreateSerializer(serializers.ModelSerializer):
    is_scrapped = serializers.SerializerMethodField()

    class Meta:
        model = Magazines
        fields = ['is_scrapped']

    def get_is_scrapped(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.scrapped_users.all()
        else:
            return False

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user in instance.scrapped_users.all():
            instance.scrapped_users.remove(user)
        else:
            instance.scrapped_users.add(user)
        return instance


class MagazineReviewsListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = MagazineComments
        fields = ['id', 'content', 'created_at', 'updated_at', 'magazines', 'user', 'name', 'reply']

    def get_name(self, obj):
        return obj.user.name


class MagazineReviewCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = MagazineComments
        fields = ['id', 'content', 'magazines', 'reply']


class MagazineReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MagazineComments
        fields = ['id', 'content']


class MagazineReviewDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = MagazineComments
        fields = ['id']
