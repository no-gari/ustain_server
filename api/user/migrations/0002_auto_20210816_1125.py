# Generated by Django 3.1.4 on 2021-08-16 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailverifier',
            options={'verbose_name': '이메일 중복 확인', 'verbose_name_plural': '이메일 중복 확인'},
        ),
        migrations.AlterModelOptions(
            name='phoneverifier',
            options={'verbose_name': '휴대폰 인증', 'verbose_name_plural': '휴대폰 인증'},
        ),
    ]
