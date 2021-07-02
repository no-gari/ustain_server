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
