# Generated by Django 2.2.4 on 2019-09-02 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aapp', '0016_auto_20190204_0818'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('data', models.TextField(null=True)),
                ('data_type', models.CharField(max_length=20, null=True)),
                ('author', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='RawScan',
        ),
    ]
