from django.db import models


# Create your models here.
class WechatGroupFile(models.Model):
    id = models.CharField(max_length=32)  # id
    file_name = models.CharField(max_length=64)  # 文件名
