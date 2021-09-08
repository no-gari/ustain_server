# Generated by Django 3.1.4 on 2021-09-06 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0007_auto_20210906_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='magazines',
            name='brand',
            field=models.CharField(blank=True, help_text='클레이풀 상의 브랜드에 해당하는 ID를 입력해주세요.', max_length=32, null=True, verbose_name='브랜드 ID'),
        ),
    ]
