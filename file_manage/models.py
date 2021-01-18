from django.db import models


# Create your models here.
class WechatGroupFile(models.Model):
    file_id = models.AutoField('编号', primary_key=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    file_name = models.CharField('文件名', max_length=64, null=False)
    remark = models.CharField('备注', max_length=64, null=True, default='')

    class Meta:
        verbose_name = '微信-群文件信息'
        verbose_name_plural = '微信-群文件列表'

    def __str__(self):
        return self.file_name


class GroupMember(models.Model):
    wx_id = models.CharField('微信号', max_length=64, null=False, primary_key=True)
    create_time = models.DateTimeField('注册时间', auto_now_add=True)

    class Meta:
        verbose_name = '微信-群文件-用户信息'
        verbose_name_plural = '微信-群文件-用户列表'

    def __str__(self):
        return self.wx_id
