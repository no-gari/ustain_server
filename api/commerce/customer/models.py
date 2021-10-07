from api.user.models import User
from django.db import models


class UserShipping(models.Model):
    user = models.ForeignKey(User, verbose_name='유저', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='이름', max_length=32, default=user.name)
    big_address = models.CharField(max_length=2048, verbose_name='')
    small_address = models.CharField(null=True, blank=True, max_length=2048)
    postal_code = models.CharField(max_length=32, verbose_name='우편 번호')
    phone_number = models.CharField(max_length=32, verbose_name='휴대폰')
    is_default = models.BooleanField(default=False, verbose_name='기본 배송지 설정')
