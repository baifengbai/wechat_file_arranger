# Generated by Django 3.0.7 on 2021-01-15 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WechatGroupFile',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=64)),
            ],
        ),
    ]