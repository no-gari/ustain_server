from api.user.models import User
from django.db import models


class UserShipping(models.Model):
    user = models.ForeignKey(User, verbose_name='유저', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='이름', max_length=32, default=user.name)
    big_address = models.CharField(max_length=2048, verbose_name='기본 주소')
    small_address = models.CharField(null=True, blank=True, max_length=2048, verbose_name='상세 주소')
    postal_code = models.CharField(max_length=32, verbose_name='우편 번호')
    phone_number = models.CharField(max_length=32, verbose_name='휴대폰')
    is_default = models.BooleanField(default=False, verbose_name='기본 배송지 설정')

    class Meta:
        verbose_name = '유저 배송지'
        verbose_name_plural = '유저 배송지'

    def __str__(self):
        return self.user.name + '의 배송지' + str(self.id)


class ShippingRequest(models.Model):
    content = models.CharField(verbose_name='요구사항', max_length=64)

    class Meta:
        verbose_name = '배송 요청사항'
        verbose_name_plural = '배송 요청사항'

    def __str__(self):
        return self.content
