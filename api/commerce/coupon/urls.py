from api.commerce.coupon.views import CouponListView, CouponRetrieveView
from django.urls import path

urlpatterns = [
    path('list/', CouponListView.as_view()),
    path('<str:coupon_id>/', CouponRetrieveView.as_view()),
]
