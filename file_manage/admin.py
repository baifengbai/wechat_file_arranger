from django.contrib import admin
from file_manage.models import WechatGroupFile, GroupMember, WechatFriendInfo, Administrator

# Register your models here.
admin.site.register(WechatGroupFile)
admin.site.register(GroupMember)
admin.site.register(WechatFriendInfo)
admin.site.register(Administrator)
