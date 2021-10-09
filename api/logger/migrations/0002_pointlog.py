# Generated by Django 3.1.4 on 2021-10-09 18:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('logger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PointLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='포인트 적립/사용 내역')),
                ('points', models.IntegerField(verbose_name='포인트 적립/사용 금액')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성일시')),
                ('usage', models.CharField(choices=[('USED', '사용'), ('GAIN', '적립')], default='GAIN', max_length=4)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='고객')),
            ],
            options={
                'verbose_name': '포인트 로그',
                'verbose_name_plural': '포인트 로그',
                'ordering': ['-created'],
            },
        ),
    ]
