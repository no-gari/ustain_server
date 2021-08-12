# Generated by Django 3.1.4 on 2021-08-11 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.EmailField(max_length=254, verbose_name='수신자')),
                ('title', models.CharField(max_length=256, verbose_name='제목')),
                ('body', models.TextField(verbose_name='내용')),
                ('status', models.CharField(blank=True, choices=[('S', '성공'), ('F', '실패')], editable=False, max_length=1, null=True, verbose_name='상태')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성일시')),
            ],
            options={
                'verbose_name': '이메일 로그',
                'verbose_name_plural': '이메일 로그',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='PhoneLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.CharField(max_length=11, verbose_name='수신자')),
                ('title', models.CharField(max_length=64, verbose_name='제목')),
                ('body', models.TextField(verbose_name='내용')),
                ('status', models.CharField(blank=True, choices=[('S', '성공'), ('F', '실패')], editable=False, max_length=1, null=True, verbose_name='상태')),
                ('fail_reason', models.TextField(blank=True, null=True, verbose_name='실패사유')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성일시')),
            ],
            options={
                'verbose_name': '휴대폰 로그',
                'verbose_name_plural': '휴대폰 로그',
                'ordering': ['-created'],
            },
        ),
    ]
