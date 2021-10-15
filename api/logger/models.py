from django.utils.translation import gettext_lazy as _
from api.user.models import User
from django.db import models


class LogStatus(models.TextChoices):
    SUCCESS = 'S', '성공'
    FAILED = 'F', '실패'


class EmailLog(models.Model):
    to = models.EmailField(verbose_name='수신자')
    title = models.CharField(verbose_name='제목', max_length=256)
    body = models.TextField(verbose_name='내용')
    status = models.CharField(verbose_name='상태', editable=False, max_length=1, choices=LogStatus.choices, null=True, blank=True)
    created = models.DateTimeField('생성일시', auto_now_add=True)

    class Meta:
        verbose_name = '이메일 로그'
        verbose_name_plural = verbose_name
        ordering = ['-created']

    def __str__(self):
        return self.body


class PhoneLog(models.Model):
    to = models.CharField(verbose_name='수신자', max_length=11)
    title = models.CharField(verbose_name='제목', max_length=64)
    body = models.TextField(verbose_name='내용')
    status = models.CharField(verbose_name='상태', editable=False, max_length=1, choices=LogStatus.choices, null=True, blank=True)
    fail_reason = models.TextField(verbose_name='실패사유', null=True, blank=True)
    created = models.DateTimeField(verbose_name='생성일시', auto_now_add=True)

    class Meta:
        verbose_name = '휴대폰 로그'
        verbose_name_plural = verbose_name
        ordering = ['-created']

    def __str__(self):
        return self.body


class PointLog(models.Model):
    user = models.ForeignKey(User, verbose_name='고객', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='포인트 적립/사용 내역', max_length=32)
    points = models.IntegerField(verbose_name='포인트 적립/사용 금액')
    created = models.DateTimeField(verbose_name='생성일시', auto_now_add=True)

    class UsageChoices(models.TextChoices):
        USED = 'USED', _('사용')
        GAIN = 'GAIN', _('적립')

    usage = models.CharField(
        max_length=4,
        choices=UsageChoices.choices,
        default=UsageChoices.GAIN,
    )

    class Meta:
        verbose_name = '포인트 로그'
        verbose_name_plural = '포인트 로그'
        ordering = ['-created']

    def __str__(self):
        return self.name
