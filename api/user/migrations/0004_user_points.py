# Generated by Django 3.1.4 on 2021-10-09 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_delete_social'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='points',
            field=models.IntegerField(blank=True, null=True, verbose_name='포인트'),
        ),
    ]
