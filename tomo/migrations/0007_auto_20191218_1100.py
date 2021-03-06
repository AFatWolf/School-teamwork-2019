# Generated by Django 2.2.5 on 2019-12-18 02:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tomo', '0006_auto_20191218_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tags',
            field=models.ManyToManyField(to='tomo.Tag'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 18, 2, 0, 23, 928886, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 18, 2, 0, 23, 927888, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='hosted_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 18, 2, 0, 23, 927888, tzinfo=utc)),
        ),
    ]
