from django.utils.translation import gettext_lazy as _
from api.magazine.models import upload_to
from django.db import models


class Catalog(models.Model):
    content = models.TextField(verbose_name='내용')
    title = models.CharField(max_length=255, verbose_name='제목')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    banner_image = models.ImageField(verbose_name='배너 이미지', upload_to=upload_to('catalog/image/%Y/%m/%d/'))
    collection = models.CharField(max_length=255, verbose_name='콜렉션 ID', help_text='클레이풀 상의 콜렉션에 해당하는 ID를 입력해주세요.')

    class Choices(models.TextChoices):

        MALE = 'MA', _('남자')
        FEMALE = 'FE', _('여자')
        BEAUTY = 'BE', _('뷰')

    choices = models.CharField(
        max_length=2,
        choices=Choices.choices,
        default=Choices.FEMALE,
        verbose_name='선택'
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = '카탈로그'
        verbose_name_plural = '카탈로그'
