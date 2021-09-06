# Generated by Django 3.1.4 on 2021-09-06 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0005_magazines_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='magazines',
            name='products',
            field=models.CharField(blank=True, help_text='상품 아이디를 입력해주세요. 여러 개일 경우 ","로 구분해주세요.', max_length=512, null=True, verbose_name='상품 이름'),
        ),
        migrations.AlterField(
            model_name='magazines',
            name='brand',
            field=models.CharField(blank=True, help_text='클레이풀 상의 브랜드에 해당하는 ID를 입력해주세요.', max_length=255, null=True, verbose_name='브랜드 이름'),
        ),
    ]
