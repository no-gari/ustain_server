# Generated by Django 3.1.4 on 2021-08-04 15:51

import api.magazine.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_summernote.utils
import functools


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='카테고리 이름을 입력하세요.', max_length=255, verbose_name='카테고리 이름')),
                ('mid', models.CharField(help_text='영문+숫자 조합만 가능한 카테고리의 고유값입니다.', max_length=255, unique=True, verbose_name='카테고리 고유값')),
                ('description', models.TextField(blank=True, help_text='카테고리에 대한 간단한 설명을 입력합니다.', null=True, verbose_name='카테고리 설명')),
                ('snapshot_image', models.ImageField(blank=True, help_text='해당하는 이미지 파일을 선택하세요.', null=True, upload_to='', verbose_name='이미지')),
            ],
            options={
                'verbose_name': '카테고리',
                'verbose_name_plural': '카테고리',
            },
        ),
        migrations.CreateModel(
            name='Magazines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_main', models.BooleanField(default=False, help_text='체크 하시면 어플리케이션 메인 배너에 등록 됩니다.', verbose_name='메인 배너 노출 여부')),
                ('title', models.CharField(max_length=255, verbose_name='제목')),
                ('content', models.TextField(verbose_name='내용')),
                ('hits', models.PositiveIntegerField(default=0, verbose_name='조회수')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('ipaddress', models.GenericIPAddressField()),
                ('published', models.BooleanField(default=False, help_text='해당 글을 발행하시려면 체크 해 주세요.', verbose_name='글 발행 여부')),
                ('comments_banned', models.BooleanField(default=False, help_text='댓글을 차단하시려면 체크 해 주세요.', verbose_name='댓글 차단')),
                ('categories', models.ManyToManyField(related_name='magazines', to='magazine.Categories', verbose_name='카테고리')),
                ('like_users', models.ManyToManyField(related_name='like_magazines', to=settings.AUTH_USER_MODEL, verbose_name='이 매거진을 좋아한 사람들')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성')),
            ],
            options={
                'verbose_name': '매거진',
                'verbose_name_plural': '매거진',
            },
        ),
        migrations.CreateModel(
            name='Summernote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, help_text='Defaults to filename, if left blank', max_length=255, null=True, verbose_name='원본파일명')),
                ('file', models.FileField(unique=True, upload_to=django_summernote.utils.uploaded_filepath)),
                ('ipaddress', models.GenericIPAddressField(blank=True, null=True)),
                ('magazines', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='magazine.magazines', verbose_name='매거진')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='글쓴이')),
            ],
            options={
                'verbose_name': '첨부 이미지',
                'verbose_name_plural': '첨부 이미지',
            },
        ),
        migrations.CreateModel(
            name='MagazineComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('ipaddress', models.GenericIPAddressField()),
                ('magazines', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazine.magazines', verbose_name='매거진')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'verbose_name': '댓글',
                'verbose_name_plural': '댓글',
            },
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=functools.partial(api.magazine.models._update_filename, *(), **{'path': 'file/%Y/%m/%d/'}), verbose_name='첨부 자료')),
                ('org_file_name', models.CharField(blank=True, max_length=255, verbose_name='원본파일명')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('magazines', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazine.magazines', verbose_name='매거진')),
            ],
            options={
                'verbose_name': '첨부 파일',
                'verbose_name_plural': '첨부 파일',
            },
        ),
    ]