# Generated by Django 3.1.4 on 2021-09-08 16:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='이메일'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(default=django.utils.timezone.now, max_length=11, unique=True, verbose_name='휴대폰'),
            preserve_default=False,
        ),
    ]
