# Generated by Django 2.0.10 on 2019-01-26 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aapp', '0013_auto_20190126_0552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inst',
            name='screen_last_update',
        ),
        migrations.RemoveField(
            model_name='inst',
            name='up_to_date',
        ),
    ]
