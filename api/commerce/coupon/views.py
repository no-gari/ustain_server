from api.commerce.coupon.serializers import CouponSerializer, CouponDetailSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import ValidationError
from api.clayful_client import ClayfulCouponClient


class CouponListView(ListAPIView):
    serializer_class = CouponSerializer

    def get_queryset(self):
        clayful = self.request.META['HTTP_CLAYFUL']
        clf_coupon_client = ClayfulCouponClient(auth_token=clayful)
        response = clf_coupon_client.coupon_list()
        if response.status != 200:
            raise ValidationError({'error_msg': '쿠폰 목록을 불러오는데 실패했습니다.'})
        return response.data

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise ValidationError({'error_msg': '로그인을 진행해주세요.'})
        return super().get(request, *args, **kwargs)


class CouponRetrieveView(RetrieveAPIView):
    serializer_class = CouponDetailSerializer
    lookup_field = 'coupon_id'

    def get_object(self, **kwargs):
        clayful = self.request.META['HTTP_CLAYFUL']
        clf_coupon_client = ClayfulCouponClient(auth_token=clayful)
        response = clf_coupon_client.coupon_detail(coupon_id=self.kwargs['coupon_id'])
        if response.status != 200:
            raise ValidationError({'error_msg': '쿠폰을 불러오는데 실패했습니다.'})
        return response.data

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise ValidationError({'error_msg': '로그인을 진행해주세요.'})
        return super().get(request, *args, **kwargs)
