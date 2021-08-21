from django.db import models


class CommerceBigCategories(models.Model):
    title = models.CharField(max_length=255, verbose_name='메인 카테고리 이름', help_text='메인 카테고리 이름을 입력하세요.')
    mid = models.CharField(unique=True, max_length=255, verbose_name='메인 카테고리 고유값',
                           help_text='영문+숫자 조합만 가능한 카테고리의 고유값입니다.', primary_key=True)
    description = models.TextField(blank=True, null=True, verbose_name='카테고리 설명', help_text='메인 카테고리에 대한 간단한 설명을 입력합니다.')
    snapshot_image = models.ImageField(blank=True, null=True, verbose_name='이미지', help_text='해당하는 이미지 파일을 선택하세요.')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = '메인 카테고리'
        verbose_name_plural = '메인 카테고리'


class CommerceSmallCategories(models.Model):
    big_category = models.ForeignKey(CommerceBigCategories, on_delete=models.CASCADE, verbose_name='메인 카테고리')
    title = models.CharField(max_length=255, verbose_name='세부 카테고리 이름', help_text='세부 카테고리 이름을 입력하세요.')
    mid = models.CharField(unique=True, max_length=255, verbose_name='카테고리 고유값',
                           help_text='영문+숫자 조합만 가능한 카테고리의 고유값입니다.', primary_key=True)
    description = models.TextField(blank=True, null=True, verbose_name='카테고리 설명', help_text='세부 카테고리에 대한 간단한 설명을 입력합니다.')
    snapshot_image = models.ImageField(blank=True, null=True, verbose_name='이미지', help_text='해당하는 이미지 파일을 선택하세요.')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = '세부 카테고리'
        verbose_name_plural = '세부 카테고리'
