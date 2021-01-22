import datetime

from PyWeChatSpy.PyWeChatSpy import WeChatSpy
from PyWeChatSpy.PyWeChatSpy.command import *
# from lxml import etree
# import requests
import time
# import logging
from PyWeChatSpy.PyWeChatSpy.proto import spy_pb2
# import base64
import os
from queue import Queue

# from threading import Thread
# import re
from loguru import logger
from traceback import print_exc

from util.operate_file import parse_dat_to_xor_code, download_file

from util.secret_code import get_secret_code_instance

import django
from django.db import close_old_connections

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wechat_file_arranger.settings")
django.setup()
from file_manage.models import WechatGroupFile, GroupMember, WechatFriendInfo

# import win32event
# import pywintypes
# import win32api
# from winerror import ERROR_ALREADY_EXISTS

# mutexname = "DEMO"  # 互斥体命名
# mutex = win32event.CreateMutex(None, False, mutexname)
# if win32api.GetLastError() == ERROR_ALREADY_EXISTS:
#     print('程序已启动')
#     exit(0)

# ------⭐以下内容需要自行配置⭐-----------↓
# ------⭐以下内容需要自行配置⭐-----------↓
# ------⭐以下内容需mi要自行配置⭐-----------↓

# TODO:微信掉线时是否发送警告邮件，如需使用该模块，需要在.\util\message_config.ini填写相关参数
IF_SEND_WARNING_MESSAGE_WHEN_WECHAT_LOG_OUT = False

# TODO:管理员微信id
ADMIN_ID = ["wxid_k0jgmjjy1qqm12", 'wxid_oftjmj5649kd22', "wxid_kus5f4xdn5ek22"]

# TODO:目标群群id
GROUP_ID = ["25522056057@chatroom"]

# TODO:微信文件位置
WECHAT_DIR_PATH = r"C:\Users\Administrator\Documents\WeChat Files"

# ------⭐以上内容需要自行配置⭐-----------↑
# ------⭐以上内容需要自行配置⭐-----------↑
# ------⭐以上内容需要自行配置⭐-----------↑

groups = []
my_response_queue = Queue()

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
FILE_DIR_PATH = os.path.join(DIR_PATH, r'file\yx')


def handle_response():
    while True:
        try:
            data = my_response_queue.get()
            if data.type == PROFESSIONAL_KEY:
                if not data.code:
                    logger.error(data.message)
            elif data.type == WECHAT_CONNECTED:  # 微信接入
                print(f"微信客户端已接入 port:{data.port}")
            elif data.type == HEART_BEAT:  # 心跳
                pass
            elif data.type == WECHAT_LOGIN:  # 微信登录
                spy.get_account_details()  # 获取登录账号详情
            elif data.type == WECHAT_LOGOUT:  # 微信登出
                pass
            elif data.type == CHAT_MESSAGE:  # 微信消息
                chat_message = spy_pb2.ChatMessage()
                chat_message.ParseFromString(data.bytes)
                for message in chat_message.message:
                    _type = message.type  # 消息类型 1.文本|3.图片...自行探索
                    _from = message.wxidFrom.str  # 消息发送方
                    _to = message.wxidTo.str  # 消息接收方

                    if _from.endswith("chatroom"):  # 如果在群聊中
                        _from_group_member = message.content.str.split(':\n', 1)[0]
                        content = message.content.str.split(':\n', 1)[-1]
                        _nickname = ''
                    else:
                        _from_group_member = ''
                        content = message.content.str  # 消息内容
                        _nickname = message.overview.split(' : ')[0]
                        if _nickname:
                            close_old_connections()
                            if WechatFriendInfo.objects.filter(wx_id=_from):
                                WechatFriendInfo.objects.filter(wx_id=_from).update(nickname=_nickname)
                            else:
                                WechatFriendInfo.objects.create(wx_id=_from, nickname=_nickname)

                    image_overview_size = message.imageOverview.imageSize  # 图片缩略图大小
                    image_overview_bytes = message.imageOverview.imageBytes  # 图片缩略图数据
                    # with open("img.jpg", "wb") as wf:
                    #     wf.write(image_overview_bytes)
                    overview = message.overview  # 消息缩略
                    timestamp = message.timestamp  # 消息时间戳

                    # TODO: 处理文本信息
                    if _type == 1:  # 文本消息
                        logger.info(f"{_from}: {content}")
                        if _to == "filehelper":
                            spy.send_text("filehelper", "Hello PyWeChatSpy3.0\n" + content)
                            spy.send_text(wxid=GROUP_ID[0], text='程序启动')

                        else:
                            # 来自个人
                            if not _from.endswith('chatroom'):
                                if _from in ADMIN_ID:
                                    if content in ['管理', 'manage', 'gl', 'yx', 'GL']:
                                        send_text(_from, 'http://yx.laorange.top/admin/')

                                close_old_connections()
                                if content in ['激活']:
                                    if not GroupMember.objects.filter(wx_id=_from):
                                        send_text(_from, '激活进度50%：未在群成员列表中找到您的信息。请在群里发言来完成激活')
                                    elif not WechatFriendInfo.objects.filter(wx_id=_from) and _nickname:
                                        WechatFriendInfo.objects.create(wx_id=_from, nickname=_nickname)
                                        send_text(_from, '激活成功')
                                    elif not _nickname:
                                        send_text(_from, '激活失败，请联系管理员')
                                    else:
                                        send_text(_from, "已激活，无需重复激活程序")
                                else:
                                    if not WechatFriendInfo.objects.filter(wx_id=_from) and _nickname:
                                        WechatFriendInfo.objects.create(wx_id=_from, nickname=_nickname)

                                if GroupMember.objects.filter(wx_id=_from):
                                    if content in ['文件列表', '文件', '查询', '查询文件']:
                                        secret_code = get_secret_code_instance()
                                        spy.send_text(_from, '网址10分钟内有效：\n' + 'yx.laorange.top/?s=' +
                                                      secret_code + f'&f={_from}')

                                    elif content in ['上传', 'upload', 'sc', 'Sc', 'SC']:
                                        secret_code = get_secret_code_instance()
                                        send_text(_from, 'http://yx.laorange.top/upload/?s=' + secret_code +
                                                  f"&f={_from}")

                                    time_gt = datetime.datetime.now() - datetime.timedelta(minutes=10)
                                    file_no_remark_info = WechatGroupFile.objects.filter(
                                        uploader=_from, remark='', create_time__gt=time_gt)
                                    file_no_remark_amount = len(file_no_remark_info)
                                    if content in ['取消', ' ', "空格"] and file_no_remark_amount:
                                        file_no_remark_info.update(remark=" ")
                                        uploader_nickname = WechatFriendInfo.objects.get(wx_id=_from).nickname
                                        send_text(GROUP_ID[0],
                                                  f"@{uploader_nickname} 新增了{file_no_remark_amount}个群文件",
                                                  at_wxid=_from)

                                    elif file_no_remark_amount:
                                        msg_send = f'已为{file_no_remark_amount}个文件设置备注：”{content}“'
                                        file_no_remark_info.update(remark=content)
                                        send_text(_from, msg_send)

                                        uploader_nickname = WechatFriendInfo.objects.get(wx_id=_from).nickname
                                        send_text(GROUP_ID[0],
                                                  f"@{uploader_nickname} 新增了{file_no_remark_amount}个群文件：“{content}”",
                                                  at_wxid=_from)

                                # 后期取消该提示
                                else:
                                    send_text(_from, '很抱歉，未在群成员列表中找到您的信息，您的请求已被取消。请先在群里发言')

                            # 来自群聊
                            else:
                                if _from in GROUP_ID:
                                    close_old_connections()
                                    if not GroupMember.objects.filter(wx_id=_from_group_member):
                                        GroupMember.objects.create(wx_id=_from_group_member)
                                    if content in ['文件列表', '文件', '查询', '查询文件']:
                                        send_file_list_link(_from)

                    # TODO: 图片消息
                    elif _type == 3:
                        file_path = message.file
                        print(_from, _to, file_path)
                        send_text(_from, '已收到您发送的图片，正在解析，请稍后...')

                        close_old_connections()
                        if GroupMember.objects.filter(wx_id=_from):
                            try:
                                friend_nickname = WechatFriendInfo.objects.get(wx_id=_from).nickname
                            except Exception as e:
                                print(e)
                                send_text(_from, '您的私聊查询功能尚未激活。解决办法：请向我发送”激活“')
                            else:
                                file_path = os.path.join(WECHAT_DIR_PATH, file_path)
                                # 图片命名为p+当前时间戳(精确到毫秒)的十六进制表示
                                file_name_time_now = 'p' + hex(int(time.time()*100))[2:] + '.jpg'

                                try_times = 0
                                result = False
                                while not result and try_times < 10:
                                    time.sleep(3)
                                    result = image_decode(file_path, file_name_time_now)
                                if result:
                                    uploader = _from
                                    WechatGroupFile.objects.create(file_name=file_name_time_now, uploader=uploader,
                                                                   uploader_nickname=friend_nickname)
                                    send_file(GROUP_ID[0], os.path.join(FILE_DIR_PATH, file_name_time_now))

                                    time_gt = datetime.datetime.now() - datetime.timedelta(minutes=10)
                                    file_no_remark_info = WechatGroupFile.objects.filter(
                                        uploader=_from, remark='', create_time__gt=time_gt)
                                    file_no_remark_amount = len(file_no_remark_info)
                                    send_text(_from, f"图片上传成功！您在10分钟内上传了{file_no_remark_amount}个文件/图片，" +
                                              "若仍有图片/文件需要上传请继续发送；若已全部发送完毕，请输入这" +
                                              f"{'张图片的' if file_no_remark_amount == 1 else '些文件/图片的统一'}备注：" +
                                              "如果不需要备注，请发送空格或”取消“")
                                else:
                                    send_text(_from, '图片解析失败')

                        # 后期取消该提示
                        else:
                            send_text(_from, '激活失败，未在群成员列表中找到您的信息。请在群里发言，或联系管理员')

                    # TODO: 视频消息
                    elif _type == 43:
                        print(_from, _to, message.file)
                        _type = 49

                    # TODO: XML报文消息
                    if _type == 49:
                        print(_from, content, message.file)
                        if message.file:
                            # v1.0.3 增加限制：只能通过私聊发送
                            if not _from.endswith('chatroom'):
                                close_old_connections()
                                if GroupMember.objects.filter(wx_id=_from):
                                    if friend_info := WechatFriendInfo.objects.filter(wx_id=_from):
                                        result = download_file(os.path.join(WECHAT_DIR_PATH, message.file))
                                        if result:
                                            uploader_nickname = friend_info.nickname
                                            file_name = os.path.split(message.file)[1]
                                            WechatGroupFile.objects.create(file_name=file_name,
                                                                           uploader=_from,
                                                                           uploader_nickname=uploader_nickname)

                                            send_file(GROUP_ID[0], os.path.join(FILE_DIR_PATH, file_name))

                                            time_gt = datetime.datetime.now() - datetime.timedelta(minutes=10)
                                            file_no_remark_info = WechatGroupFile.objects.filter(
                                                uploader=_from, remark='', create_time__gt=time_gt)
                                            file_no_remark_amount = len(file_no_remark_info)
                                            send_text(_from, f"文件上传成功！您在10分钟内上传了{file_no_remark_amount}个文件/图片，" +
                                                      "若仍有图片/文件需要上传请继续发送；若已全部发送完毕，请输入这" +
                                                      f"{'个文件的' if file_no_remark_amount == 1 else '些文件/图片的统一'}备注：" +
                                                      "如果不需要备注，请发送空格或”取消“")
                                        else:
                                            send_text(_from, "文件上传失败，请稍后重试或通过网页上传（向我发送“上传”可获取上传网页的网址）")

                                # 后期取消该提示
                                else:
                                    send_text(_from, '激活失败，未在群成员列表中找到您的信息。请在群里发言，或联系管理员')

            elif data.type == ACCOUNT_DETAILS:  # 登录账号详情
                if data.code:
                    account_details = spy_pb2.AccountDetails()
                    account_details.ParseFromString(data.bytes)
                    print(account_details)
                    # spy.get_contacts()  # 获取联系人列表
                else:
                    logger.warning(data.message)

            elif data.type == CONTACTS_LIST:  # 联系人列表
                if data.code:
                    contacts_list = spy_pb2.Contacts()
                    contacts_list.ParseFromString(data.bytes)
                    for contact in contacts_list.contactDetails:
                        wxid = contact.wxid.str  # 联系人wxid
                        nickname = contact.nickname.str  # 联系人昵称
                        remark = contact.remark.str  # 联系人备注
                        print(wxid, nickname, remark)
                        if wxid.endswith("chatroom"):  # 群聊
                            groups.append(wxid)
                    wxid = groups.pop()
                    print(wxid)
                else:
                    logger.error(data.message)

            elif data.type == CONTACT_DETAILS:
                if data.code:
                    contact_details_list = spy_pb2.Contacts()
                    contact_details_list.ParseFromString(data.bytes)
                    for contact_details in contact_details_list.contactDetails:
                        wxid = contact_details.wxid.str  # 联系人wxid
                        nickname = contact_details.nickname.str  # 联系人昵称
                        remark = contact_details.remark.str  # 联系人备注
                        if wxid.endswith("chatroom"):  # 判断是否为群聊
                            group_member_list = contact_details.groupMemberList  # 群成员列表
                            member_count = group_member_list.memberCount  # 群成员数量
                            for group_member in group_member_list.groupMember:  # 遍历群成员
                                member_wxid = group_member.wxid
                                member_nickname = group_member.nickname
                                print(member_wxid, member_nickname)
                            pass
                else:
                    logger.error(data.message)

            elif data.type == GET_CONTACTS_LIST and not data.code:
                logger.error(data.message)

            elif data.type == CREATE_GROUP_CALLBACK:  # 创建群聊回调
                callback = spy_pb2.CreateGroupCallback()
                callback.ParseFromString(data.bytes)
                print(callback)

            elif data.type == GROUP_MEMBER_DETAILS:  # 群成员详情
                group_member_details = spy_pb2.GroupMemberDetails()
                group_member_details.ParseFromString(data.bytes)
                print(group_member_details)

            elif data.type == GROUP_MEMBER_EVENT:
                group_member_event = spy_pb2.GroupMemberEvent()
                group_member_event.ParseFromString(data.bytes)
                print(group_member_event)

            else:
                print(data)
        except Exception as e:
            print(e)
            print_exc()


def send_file_list_link(wxid):
    secret_code = get_secret_code_instance()
    spy.send_text(wxid, '网址10分钟内有效：\n' + 'yx.laorange.top/?s=' + secret_code)


spy = WeChatSpy(response_queue=my_response_queue, key="", logger=logger)


def log_in_wechat():
    def log_in_wechat_main():
        try:
            pid = spy.run(r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe")
            handle_response()
            print("after handle_response")
        except OSError:
            pass

    from threading import Thread
    thread1 = Thread(target=log_in_wechat_main)
    thread1.start()
    return spy


def send_text(wxid: str, text: str, at_wxid: str = "", port: int = 0):
    spy.send_text(wxid, text, at_wxid, port)


def send_file(wxid: str, file_path: str, port: int = 0):
    spy.send_file(wxid, file_path, port)


def image_decode(dat_path, output_file_name):
    xor_value = parse_dat_to_xor_code(dat_path)
    # dat_dir_path, dat_name = os.path.split(dat_path)[0], os.path.split(dat_path)[1]
    # target_path = r'F:\Users\Tencent Files\WeChat Files\image'
    if xor_value:
        try:
            target_path = FILE_DIR_PATH
            with open(dat_path, "rb") as dat_read:
                if not os.path.exists(target_path):
                    os.makedirs(target_path)
                out = target_path + "\\" + output_file_name
                with open(out, "wb") as png_write:
                    for now in dat_read:
                        for nowByte in now:
                            newByte = nowByte ^ xor_value
                            png_write.write(bytes([newByte]))
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False


if not os.path.exists('occupy.pid'):
    log_in_wechat()
    with open('occupy.pid', 'wt') as occ:
        occ.write('occupy')
else:
    logger.warning('检测到occupy.pid，请在运行微信前删除该文件')

if __name__ == '__main__':
    log_in_wechat()
    print(spy)
    print(1)
    # spy.get_contact_details("20646587964@chatroom")
