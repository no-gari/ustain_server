# Generated by Django 3.1.4 on 2021-08-04 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_categories_profile_userlevel'),
        ('magazine', '0002_delete_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magazines',
            name='categories',
            field=models.ManyToManyField(related_name='magazines', to='user.Categories', verbose_name='카테고리'),
        ),
    ]