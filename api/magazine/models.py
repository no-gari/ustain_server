from django_summernote.utils import get_attachment_storage, get_attachment_upload_to
from django_summernote import models as summermodel
from api.user.models import Categories
from api.user.models import User
from functools import partial
from django.db import models
from enum import Enum
import uuid
import os


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


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]


class Magazines(models.Model):
    categories = models.ManyToManyField(Categories, verbose_name='카테고리', related_name='magazines')
    is_main = models.BooleanField(default=False, verbose_name='메인 배너 노출 여부', help_text='체크 하시면 어플리케이션 메인 배너에 등록 됩니다.')
    banner_image = models.ImageField(verbose_name='배너 이미지', upload_to=upload_to('image/%Y/%m/%d/'), blank=True, null=True)
    published = models.BooleanField(default=False, verbose_name='글 발행 여부', help_text='해당 글을 발행하시려면 체크 해 주세요.')
    comments_banned = models.BooleanField(default=False, verbose_name='댓글 차단', help_text='댓글을 차단하시려면 체크 해 주세요.')
    like_users = models.ManyToManyField(User, related_name='like_magazines', verbose_name='이 매거진을 좋아한 사람들')
    scrapped_users = models.ManyToManyField(User, related_name='scrapped_magazines', verbose_name='이 매거진을 스크랩한 사람들')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    hits = models.PositiveIntegerField(default=0, verbose_name='조회수')
    title = models.CharField(max_length=255, verbose_name='제목')
    content = models.TextField(verbose_name='내용')


    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = '매거진'
        verbose_name_plural = '매거진'


class MagazineComments(models.Model):
    magazines = models.ForeignKey(Magazines, on_delete=models.CASCADE, related_name='magazine_comments', verbose_name='매거진')
    content = models.TextField(verbose_name='내용')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply', null=True, blank=True, verbose_name='대댓글')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    def __str__(self):
        return str(self.magazines.title) + ' 의 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글'


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
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='글쓴이')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = '첨부 이미지'
        verbose_name_plural = '첨부 이미지'
