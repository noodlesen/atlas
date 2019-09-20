# Generated by Django 2.2.4 on 2019-09-19 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aapp', '0020_auto_20190914_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiCall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api', models.CharField(max_length=50, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('success', models.BooleanField(null=True)),
                ('response', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='aapp.RawData')),
            ],
        ),
    ]