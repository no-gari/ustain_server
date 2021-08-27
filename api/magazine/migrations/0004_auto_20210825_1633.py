# Generated by Django 3.1.4 on 2021-08-25 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0003_magazines_scrapped_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='magazinecomments',
            name='reply',
        ),
        migrations.AddField(
            model_name='magazinecomments',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='magazine.magazinecomments', verbose_name='대댓글'),
        ),
    ]
