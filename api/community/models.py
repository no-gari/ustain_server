from django.db import models

# Create your models here.
from django.db import models
from enum import Enum
from api.user.models import User
from django_summernote import models as summermodel
from django_summernote.utils import get_attachment_storage, get_attachment_upload_to
import os
from functools import partial
import uuid
from api.user.models import Categories


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]


class QnaCategories(models.Model):
    class QnaOptions(ChoiceEnum):
        all = '모든 사용자'
        join = '가입한 사용자'
        super = '관리자만'
        other = '기타'



    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'QnA 문의'
        verbose_name_plural = 'QnA 문의'


class MagazineComments(models.Model):
    magazines = models.ForeignKey(Magazines, on_delete=models.CASCADE, verbose_name='매거진')
    content = models.TextField(verbose_name='내용')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    ipaddress = models.GenericIPAddressField()

    def __str__(self):
        return str(self.magazines.title) + ' 의 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글'


def _update_filename(instance, filename, path):
    from datetime import datetime
    today = datetime.now()
    path = path.replace('%Y', today.strftime('%Y'))
    path = path.replace('%m', today.strftime('%m'))
    path = path.replace('%d', today.strftime('%d'))

    file_ext = filename.split('.')
    file_ext = file_ext[len(file_ext) - 1]

    filename = "{}.{}".format(uuid.uuid4(), file_ext)

    return os.path.join(path, filename)


def upload_to(path):
    return partial(_update_filename, path=path)


class Files(models.Model):
    magazines = models.ForeignKey(Magazines, on_delete=models.CASCADE, verbose_name='매거진')
    file = models.FileField(upload_to=upload_to('file/%Y/%m/%d/'), verbose_name='첨부 자료')
    org_file_name = models.CharField(max_length=255, blank=True, verbose_name='원본파일명')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    def __str__(self):
        return str(self.document.title) + ' 의 첨부 파일'

    class Meta:
        verbose_name = '첨부 파일'
        verbose_name_plural = '첨부 파일'


class Summernote(summermodel.AbstractAttachment):
    magazines = summermodel.models.ForeignKey(Magazines, null=True, blank=True, verbose_name='매거진',
                                              on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='원본파일명',
                            help_text="Defaults to filename, if left blank")
    file = models.FileField(
        upload_to=get_attachment_upload_to(),
        storage=get_attachment_storage(),
        unique=True
    )
    ipaddress = models.GenericIPAddressField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='글쓴이')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = '첨부 이미지'
        verbose_name_plural = '첨부 이미지'
