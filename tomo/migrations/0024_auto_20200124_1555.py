# Generated by Django 2.2.5 on 2020-01-24 06:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tomo', '0023_merge_20200124_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 24, 6, 55, 28, 266198, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 24, 6, 55, 28, 264203, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='hosted_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 24, 6, 55, 28, 263206, tzinfo=utc)),
        ),
    ]
