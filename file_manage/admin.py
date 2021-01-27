from django.contrib import admin
from file_manage.models import WechatGroupFile, GroupMember, WechatFriendInfo, Administrator


# Register your models here.
class WechatGroupFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'remark', 'uploader_nickname', "create_time")
    readonly_fields = ("file_name", "create_time")


class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ("wx_id", "nickname", "update_time")
    readonly_fields = ("wx_id", "create_time", "update_time")


class WechatFriendInfoAdmin(admin.ModelAdmin):
    list_display = ("wx_id", "nickname", "update_time")
    readonly_fields = ("wx_id", "update_time")


class AdministratorAdmin(admin.ModelAdmin):
    list_display = ("wx_id", "remark")
    readonly_fields = ("update_time", )


admin.site.register(WechatGroupFile, WechatGroupFileAdmin)
admin.site.register(GroupMember, GroupMemberAdmin)
admin.site.register(WechatFriendInfo, WechatFriendInfoAdmin)
admin.site.register(Administrator)
