# Generated by Django 3.2.8 on 2021-10-26 17:05

import api.user.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('title', models.CharField(help_text='카테고리 이름을 입력하세요.', max_length=255, verbose_name='카테고리 이름')),
                ('mid', models.CharField(help_text='영문+숫자 조합만 가능한 카테고리의 고유값입니다.', max_length=255, primary_key=True, serialize=False, unique=True, verbose_name='카테고리 고유값')),
                ('description', models.TextField(blank=True, help_text='카테고리에 대한 간단한 설명을 입력합니다.', null=True, verbose_name='카테고리 설명')),
                ('snapshot_image', models.ImageField(blank=True, help_text='해당하는 이미지 파일을 선택하세요.', null=True, upload_to='', verbose_name='이미지')),
            ],
            options={
                'verbose_name': '소셜 카테고리',
                'verbose_name_plural': '소셜 카테고리',
            },
        ),
        migrations.CreateModel(
            name='EmailVerifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='이메일')),
                ('code', models.CharField(max_length=6, verbose_name='인증번호')),
                ('token', models.CharField(max_length=40, verbose_name='토큰')),
                ('created', models.DateTimeField(verbose_name='생성일시')),
            ],
            options={
                'verbose_name': '이메일 중복 확인',
                'verbose_name_plural': '이메일 중복 확인',
            },
        ),
        migrations.CreateModel(
            name='PhoneVerifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=11, verbose_name='휴대폰번호')),
                ('code', models.CharField(max_length=6, verbose_name='인증번호')),
                ('token', models.CharField(max_length=40, verbose_name='토큰')),
                ('created', models.DateTimeField(verbose_name='생성일시')),
            ],
            options={
                'verbose_name': '휴대폰 인증',
                'verbose_name_plural': '휴대폰 인증',
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='이미지')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(blank=True, max_length=16, null=True, verbose_name='닉네임')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='이메일')),
                ('email_verify', models.BooleanField(default=False, verbose_name='이메일 인증')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='휴대폰')),
                ('profile_article', models.CharField(blank=True, max_length=512, null=True, verbose_name='프로필 정보')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='생일')),
                ('sex_choices', models.CharField(choices=[('MA', '남자'), ('FE', '여자')], default='MA', max_length=2)),
                ('categories', models.ManyToManyField(to='user.Categories', verbose_name='관심 카테고리')),
                ('groups', models.ManyToManyField(blank=True, null=True, to='user.UserGroup', verbose_name='속한 그룹')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '유저',
                'verbose_name_plural': '유저',
                'ordering': ['-date_joined'],
            },
            managers=[
                ('objects', api.user.models.UserManager()),
            ],
        ),
    ]
