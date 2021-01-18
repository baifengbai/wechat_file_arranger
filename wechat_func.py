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

# from file_manage.models import WechatGroupFile
from util.download_file import download_file
# from util.mysql_util import add_file_to_mysql
# from util.operate_file import InputFileData

from util.secret_code import get_secret_time_code

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wechat_file_arranger.settings")
django.setup()
from file_manage.models import WechatGroupFile, GroupMember

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

# TODO:是否接受图片，如需使用该功能，请参考https://blog.csdn.net/zhanglw882/article/details/110221075 来配置xor_value
IF_RECEIVE_IMAGE = True
xor_value = 0x14

# TODO:管理员微信id
ADMIN_ID = ["wxid_k0jgmjjy1qqm12", 'wxid_oftjmj5649kd22', "wxid_kus5f4xdn5ek22"]

# TODO:目标群群id
GROUP_ID = ["25522056057@chatroom"]

# ------⭐以上内容需要自行配置⭐-----------↑
# ------⭐以上内容需要自行配置⭐-----------↑
# ------⭐以上内容需要自行配置⭐-----------↑

groups = []
WECHAT_PROFILE = r"D:\Documents\WeChat Files"
my_response_queue = Queue()

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
FILE_DIR_PATH = os.path.join(DIR_PATH, 'file')

WECHAT_DIR_PATH = r"C:\Users\Administrator\Documents\WeChat Files"


class InputtingImage:
    def __init__(self):
        self.inputting = 0
        self.image_path = ''
        self.image_name = ''

    def start_input(self, image_path):
        self.inputting = 1
        self.image_path = image_path

    def input_name(self, image_name):
        self.image_name = image_name


inputting_image_status = InputtingImage()


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
                        _from_group_member = message.content.str.split(':\n', 2)[0]
                        content = message.content.str.split(':\n', 2)[-1]
                    else:
                        _from_group_member = ''
                        content = message.content.str  # 消息内容

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

                        else:
                            if _from in ADMIN_ID:
                                if content in ['文件列表', '文件', '查询', '查询文件']:
                                    send_file_list_link(_from)
                                elif content in ['管理', 'manage', 'gl', 'yx']:
                                    send_text(_from, 'http://yx.laorange.top/admin/')

                            elif _from in GROUP_ID:
                                if content in ['文件列表', '文件', '查询', '查询文件']:
                                    send_file_list_link(_from)
                                    try:
                                        GroupMember.objects.create(wx_id=_from_group_member)
                                    except:
                                        pass

                    # TODO: 图片消息
                    elif _type == 3:
                        file_path = message.file
                        print(_from, _to, file_path)
                        file_path = os.path.join(WECHAT_PROFILE, file_path)
                        time.sleep(10)
                        file_name_time_now = time.ctime().replace(' ', '_') + '.jpg'
                        spy.decrypt_image(file_path, os.path.join(FILE_DIR_PATH, file_name_time_now))
                        WechatGroupFile.objects.create(file_name=file_name_time_now)

                    # TODO: 视频消息
                    elif _type == 43:
                        print(_from, _to, message.file)
                        # if message.file:
                        #     if _from in ADMIN_ID or _from in GROUP_ID:  # 管理员私发&任意群文件均视为有效
                        #         result = download_file(os.path.join(WECHAT_DIR_PATH, message.file))
                        #         if result:
                        #             send_file_list_link(_from)

                    # TODO: XML报文消息
                    elif _type == 49:
                        print(_from, content, message.file)
                        if message.file:
                            if _from in ADMIN_ID or _from in GROUP_ID:  # 管理员私发&任意群文件均视为有效
                                result = download_file(os.path.join(WECHAT_DIR_PATH, message.file))
                                if result:
                                    WechatGroupFile.objects.create(file_name=os.path.split(message.file)[1])
                                    send_file_list_link(_from)

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
    secret_code = get_secret_time_code()
    spy.send_text(wxid, '网址5分钟内有效：\n' + 'yx.laorange.top/?s=' + secret_code)


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


if not os.path.exists('occupy.pid'):
    log_in_wechat()
with open('occupy.pid', 'wt') as occ:
    occ.write('occupy')

if __name__ == '__main__':
    log_in_wechat()
    print(spy)
    print(1)
    # spy.get_contact_details("20646587964@chatroom")
