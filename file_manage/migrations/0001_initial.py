# Generated by Django 3.0.7 on 2021-01-22 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('wx_id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='微信号')),
                ('remark', models.CharField(default='', max_length=64, verbose_name='备注')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='信息更新时间')),
            ],
            options={
                'verbose_name': '微信文件管理-管理员',
                'verbose_name_plural': '微信文件管理-管理员列表',
                'ordering': ('update_time__date',),
            },
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('wx_id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='微信号')),
                ('nickname', models.CharField(default='', max_length=64, verbose_name='昵称或备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '微信-群文件-用户信息',
                'verbose_name_plural': '微信-群文件-用户列表',
                'ordering': ('update_time__date',),
            },
        ),
        migrations.CreateModel(
            name='WechatFriendInfo',
            fields=[
                ('wx_id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='微信号')),
                ('nickname', models.CharField(default='', max_length=64, verbose_name='昵称或备注')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='信息更新时间')),
            ],
            options={
                'verbose_name': '微信-好友信息',
                'verbose_name_plural': '微信-好友列表',
                'ordering': ('update_time__date',),
            },
        ),
        migrations.CreateModel(
            name='WechatGroupFile',
            fields=[
                ('file_id', models.AutoField(primary_key=True, serialize=False, verbose_name='编号')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('file_name', models.CharField(max_length=64, verbose_name='文件名')),
                ('remark', models.CharField(default='', max_length=64, verbose_name='备注')),
                ('uploader', models.CharField(default='', max_length=64, verbose_name='上传者')),
                ('uploader_nickname', models.CharField(default='', max_length=64, verbose_name='上传者昵称')),
            ],
            options={
                'verbose_name': '微信-群文件信息',
                'verbose_name_plural': '微信-群文件列表',
                'ordering': ('create_time__date',),
            },
        ),
    ]
