# Generated by Django 2.2.5 on 2020-01-13 01:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tomo', '0009_auto_20200113_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 13, 1, 6, 3, 660162, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 13, 1, 6, 3, 660162, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='hosted_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 13, 1, 6, 3, 660162, tzinfo=utc)),
        ),
    ]
