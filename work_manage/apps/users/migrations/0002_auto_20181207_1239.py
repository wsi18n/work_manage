# Generated by Django 2.1.1 on 2018-12-07 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='is_able',
            field=models.BooleanField(default=True, verbose_name='是否启用'),
        ),
        migrations.AddField(
            model_name='post',
            name='is_able',
            field=models.BooleanField(default=True, verbose_name='是否启用'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_able',
            field=models.BooleanField(default=True, verbose_name='是否启用'),
        ),
    ]
