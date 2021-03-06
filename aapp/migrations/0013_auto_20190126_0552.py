# Generated by Django 2.0.10 on 2019-01-26 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aapp', '0012_rawscan_query'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inst',
            old_name='hist_last_updated',
            new_name='details_last_update',
        ),
        migrations.RenameField(
            model_name='inst',
            old_name='screen_last_updated',
            new_name='hist_last_update',
        ),
        migrations.RemoveField(
            model_name='inst',
            name='history_scanned',
        ),
        migrations.RemoveField(
            model_name='inst',
            name='screen_scanned',
        ),
        migrations.RemoveField(
            model_name='rawscan',
            name='query',
        ),
        migrations.AddField(
            model_name='inst',
            name='details',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='inst',
            name='screen_last_update',
            field=models.DateTimeField(null=True),
        ),
    ]
