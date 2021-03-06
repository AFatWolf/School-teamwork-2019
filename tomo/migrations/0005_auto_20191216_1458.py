# Generated by Django 2.2.5 on 2019-12-16 05:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tomo', '0004_auto_20191213_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 16, 5, 58, 5, 878276, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 16, 5, 58, 5, 878276, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='hosted_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 16, 5, 58, 5, 878276, tzinfo=utc)),
        ),
    ]
