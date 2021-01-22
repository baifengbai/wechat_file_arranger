from django.db import models


# Create your models here.
class WechatGroupFile(models.Model):
    file_id = models.AutoField('编号', primary_key=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    file_name = models.CharField('文件名', max_length=64, null=False)
    remark = models.CharField('备注', max_length=64, default='')
    uploader = models.CharField('上传者', max_length=64, default='')
    uploader_nickname = models.CharField('上传者昵称', max_length=64, default='')
    watch_times = models.IntegerField('查看次数', default=0)

    class Meta:
        verbose_name = '微信-群文件信息'
        verbose_name_plural = '微信-群文件列表'

    def __str__(self):
        return self.remark if self.remark else self.file_name


class GroupMember(models.Model):
    wx_id = models.CharField('微信号', max_length=64, null=False, primary_key=True)
    nickname = models.CharField('昵称或备注', max_length=64, default='')
    create_time = models.DateTimeField('注册时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '微信-群文件-用户信息'
        verbose_name_plural = '微信-群文件-用户列表'

    def __str__(self):
        return self.nickname if self.nickname else self.wx_id


class WechatFriendInfo(models.Model):
    wx_id = models.CharField('微信号', max_length=64, null=False, primary_key=True)
    nickname = models.CharField('昵称或备注', max_length=64, default='')
    update_time = models.DateTimeField('信息更新时间', auto_now=True)

    class Meta:
        verbose_name = '微信-好友信息'
        verbose_name_plural = '微信-好友列表'

    def __str__(self):
        return self.nickname if self.nickname else self.wx_id


class Administrator(models.Model):
    wx_id = models.CharField('微信号', max_length=64, null=False, primary_key=True)
    remark = models.CharField('备注', max_length=64, default='')
    update_time = models.DateTimeField('信息更新时间', auto_now=True)

    class Meta:
        verbose_name = '微信文件管理-管理员'
        verbose_name_plural = '微信文件管理-管理员列表'

    def __str__(self):
        return self.remark if self.remark else self.wx_id
