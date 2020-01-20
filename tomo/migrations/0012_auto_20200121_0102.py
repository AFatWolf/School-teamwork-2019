# Generated by Django 2.2.5 on 2020-01-20 16:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tomo', '0011_auto_20200121_0047'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='lat',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='event',
            name='lng',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 20, 16, 2, 44, 268221, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 20, 16, 2, 44, 263180, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='hosted_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 20, 16, 2, 44, 263180, tzinfo=utc)),
        ),
    ]
