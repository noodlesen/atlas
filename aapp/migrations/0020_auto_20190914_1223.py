# Generated by Django 2.2.4 on 2019-09-14 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aapp', '0019_auto_20190914_1159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fundamentalevent',
            old_name='ticker',
            new_name='symbol',
        ),
    ]
