# Generated by Django 2.0.10 on 2019-01-19 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aapp', '0003_auto_20190117_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inst', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='aapp.Inst')),
                ('portfolio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='aapp.Portfolio')),
            ],
        ),
    ]
