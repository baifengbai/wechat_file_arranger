from django.contrib import admin
from file_manage.models import WechatGroupFile, GroupMember, WechatFriendInfo, Administrator


# Register your models here.
class WechatGroupFileAdmin(admin.ModelAdmin):
    readonly_fields = ("file_name", "create_time")


class GroupMemberAdmin(admin.ModelAdmin):
    readonly_fields = ("wx_id", "create_time", "update_time")


class WechatFriendInfoAdmin(admin.ModelAdmin):
    readonly_fields = ("wx_id", "update_time")


admin.site.register(WechatGroupFile, WechatGroupFileAdmin)
admin.site.register(GroupMember, GroupMemberAdmin)
admin.site.register(WechatFriendInfo, WechatFriendInfoAdmin)
admin.site.register(Administrator)
