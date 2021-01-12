from PyWeChatSpy_v2.PyWeChatSpy import WeChatSpy
from PyWeChatSpy_v2.PyWeChatSpy.command import *
# from lxml import etree
import requests
import time
import os
import re
from loguru import logger
from util.func_apscheduler import do_at_sometime
from util.operate_file import move_wechat_file
from util.input_file_data import InputFileData, search_file_by_id, delete_file_by_id

# ------⭐以下内容需要自行配置⭐-----------↓
# ------⭐以下内容需要自行配置⭐-----------↓
# ------⭐以下内容需要自行配置⭐-----------↓

# 微信掉线时是否发送警告邮件，如需使用该模块，需要在.\util\message_config.ini填写相关参数
IF_SEND_WARNING_MESSAGE_WHEN_WECHAT_LOG_OUT = False

# 是否接受图片，如需使用该功能，请参考https://blog.csdn.net/zhanglw882/article/details/110221075 来配置xor_value
IF_RECEIVE_IMAGE = True
xor_value = 0x87

# 管理员微信id
ADMIN_ID = ["wxid_k0jgmjjy1qqm12"]

# 目标群群id
GROUP_ID = ["25522056057@chatroom"]

# ------⭐以上内容需要自行配置⭐-----------↑
# ------⭐以上内容需要自行配置⭐-----------↑
# ------⭐以上内容需要自行配置⭐-----------↑

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
FILE_DIR_PATH = os.path.join(DIR_PATH, 'file')


class InputtingImage:
    def __init__(self):
        self.inputting = 0
        self.image_path = ''
        self.image_name = ''

    def start_input(self, image_path):
        self.inputting = 1
        self.image_path = image_path

    def input_name_and_then_parse(self, image_name):
        self.image_name = image_name
        result = image_decode(self.image_path, self.image_name)
        return result


inputting_image_status = InputtingImage()

# 原example自带
contact_list = []
chatroom_list = []


def my_proto_parser(data):
    global inputting_image_status

    if data.type == WECHAT_CONNECTED:
        print("-" * 10, "微信连接成功", "-" * 10)
        # print("-"*10, "展示登录二维码", "-"*10)
        # spy.show_qrcode()
    elif data.type == WECHAT_LOGIN:
        print("-" * 10, "微信登录成功", "-" * 10)
        spy.get_login_info()
    elif data.type == WECHAT_LOGOUT:
        print("-" * 10, "微信登出", "-" * 10)
        if IF_SEND_WARNING_MESSAGE_WHEN_WECHAT_LOG_OUT:
            from util.send_message import send_mail
            send_mail()  # wechat登出警告信
    elif data.type == LOGIN_INFO:
        print("-" * 10, "登录信息", "-" * 10)
        print(data.login_info.wxid)
        print(data.login_info.nickname)
        print(data.login_info.wechatid)
        print(data.login_info.phone)
        print(data.login_info.profilephoto)
    elif data.type == CONTACTS:
        print("-" * 10, "联系人列表", "-" * 10)
        for contact in data.contact:
            print(contact.wxid, contact.nickname)
            if contact.wxid.startswith("gh_"):
                # 过滤公众号
                pass
            elif contact.wxid.endswith("chatroom"):
                # 群聊
                chatroom_list.append(contact.wxid)
            else:
                # 普通联系人
                contact_list.append(contact.wxid)
        print("-" * 10, f"共{len(contact_list)}个联系人,{len(chatroom_list)}个群", "-" * 10)

    elif data.type == MESSAGE:
        # 消息
        for message in data.message:
            from_whom = message.wxid1
            # logger.info(f"{from_whom}: {message.content}")
            if message.type == 1:
                logger.info(f"{from_whom}: {message.content}")
                if message.wxid1 == "filehelper":
                    pass
                else:
                    if message.wxid1 in ADMIN_ID:
                        if inputting_image_status.inputting:
                            result = inputting_image_status.input_name_and_then_parse(message.content)
                            if result:
                                input_file_data_instance = InputFileData(inputting_image_status.image_name + '.png')
                                input_file_data_instance.output_func()
                                time.sleep(1)
                                send_file(GROUP_ID[0], os.path.join(DIR_PATH, '文件列表.txt'))
                            else:
                                send(message.wxid1, '图片解析失败，进程已取消')
                                inputting_image_status.inputting = 0
                        elif search_result := re.search(r'^删除(\d{8}$)', message.content):
                            file_id = search_result.group(1)
                            file_name = delete_file_by_id(file_id)
                            if file_name:
                                try:
                                    os.remove(os.path.join(FILE_DIR_PATH, file_name))
                                    send(message.wxid1, f'已删除文件：{file_name}({file_id})”')
                                except Exception as e:
                                    print(e)
                                    send(message.wxid1, f'删除文件时出错，请检查file.ini中的配置”')


                    elif message.wxid1 in GROUP_ID:
                        if re.search(r'^\d{8}$', message.content):
                            file_name = search_file_by_id(message.content)
                            if file_name:
                                try:
                                    send_file(message.wxid1, os.path.join(FILE_DIR_PATH, file_name))
                                except Exception as e:
                                    print(e)
                                    send(message.wxid1, '查询时出错')
                            else:
                                send(message.wxid1, '没有找到这个文件')
                        if message.content in ['文件列表', '文件', '查询', '查询文件']:
                            send_file(message.wxid1, os.path.join(DIR_PATH, '文件列表.txt'))

            elif message.type == 3:
                if IF_RECEIVE_IMAGE:
                    if message.wxid1 in ADMIN_ID:
                        try:
                            logger.info("图片消息 " + f"{from_whom}")
                            inputting_image_status.start_input(message.file)
                            send(message.wxid1, "请输入这张图片的名字，以便调用")
                            continue
                        except Exception as e:
                            print(e)
            elif message.type == 37:
                print("-" * 10, "好友请求消息", "-" * 10)
                # 好友请求消息
                # obj = etree.XML(message.content)
                # encryptusername, ticket = obj.xpath("/msg/@encryptusername")[0], obj.xpath("/msg/@ticket")[0]
                # spy.accept_new_contact(encryptusername, ticket)  # 接收好友请求(付费)
                continue
            elif message.type == 49 and "邀请你加入群聊" in message.content:
                print("-" * 10, "群邀请", "-" * 10)
                # xml = etree.XML(message.content)
                # url = xml.xpath("/msg/appmsg/url/text()")
                # if url:
                #     url = url[0]
                #     print(url)
                #     spy.get_chatroom_invite_url(message.wxid1, url)  # 自动进群(尚未实现)
                # else:
                #     print("群邀请链接获取失败：解析xml失败")
                continue
            else:
                print("-" * 10, f"其他消息:{message.type}", "-" * 10)
                if message.type == 49:
                    if message.file:
                        if message.wxid1 in ADMIN_ID or message.wxid1 in GROUP_ID:  # 管理员私发&任意群文件均视为有效
                            def move_file():
                                if_succeed = move_wechat_file(message.file)
                                if if_succeed:
                                    file_name = os.path.split(message.file)[1]
                                    input_file_data_instance = InputFileData(file_name)
                                    input_file_data_instance.output_func()
                                    time.sleep(1)
                                    send_file(GROUP_ID[0], os.path.join(DIR_PATH, '文件列表.txt'))

                            do_at_sometime(move_file, 10, countdown=True)
            # print("来源1:", message.wxid1)
            # print("来源2:", message.wxid2)
            # print("消息头:", message.head)
            # print("消息内容:", message.content)
    elif data.type == QRCODE:
        print("-" * 10, "登录二维码", "-" * 10)
        print(data.qrcode.qrcode)
    elif data.type == CONTACT_EVENT:
        print("-" * 10, "联系人事件", "-" * 10)
        print(data)
    elif data.type == CHATROOM_MEMBERS:
        print("-" * 10, "群成员列表", "-" * 10)
        # type: 304
        # pid: 11384
        # uuid: "c072113b-3920-4de0-ba1e-6445bde68f2a"
        # chatroom_member {
        #   wxid: "******41@chatroom"
        #   contact {
        #     wxid: "wxid_d******11"
        #     nickname: "CC"
        #     wechatid: "j******"
        #   }
        #   contact {
        #     wxid: "******"
        #     nickname: "Xia"
        #   }
        #   contact {
        #     wxid: "wxid_9b******12"
        #     nickname: "******"
        #   }
        #   contact {
        #     wxid: "********"
        #     nickname: "*******"
        #   }
        # }
        chatroom_member = data.chatroom_member
        chatroom_wxid = chatroom_member.wxid
        print(chatroom_wxid)
        for member in chatroom_member.contact:
            print(member.wxid, member.nickname)
            # 添加群成员为好友(付费)
            # 高风险操作 容易引发微信风控
            # spy.add_contact(
            #     member.wxid,
            #     chatroom_wxid,
            #     f"你好{member.nickname},这是来自PyWeChatSpy(https://zhuanlan.zhihu.com/p/118674498)的问候",
            #     ADD_CONTACT_A)
    elif data.type == CONTACT_DETAILS:
        logger.info("联系人详情")
        # user_list = get_user_list_wechat_id()
        for details in data.contact:
            # if details.wxid in user_list:
            #     set_remark(details.wxid, details.remark)
            print(details.wxid)
            print(details.nickname)
            print(details.wechatid)
            print(details.remark)
            print(details.profilephoto)
            print(details.profilephoto_hd)
            print(details.sex)
            print(details.whats_up)
            print(details.country)
            print(details.province)
            print(details.city)
            print(details.source)
    elif data.type == CONTACT_STATUS:
        print("-" * 10, "联系人状态", "-" * 10)
        print(data)
    elif data.type == HEART_BEAT:
        # 心跳
        pass
    elif data.type == SET_REMARK:
        print("-" * 10, "备注设置完成", "-" * 10)
        print(data)
    elif data.type == CONTACT_STATUS:
        print("-" * 10, "联系人状态", "-" * 10)
        print(data)
    elif data.type == GET_CHATROOM_INVITATION_URL:
        print("-" * 10, "群邀请链接", "-" * 10)
        for message in data.message:
            if message.type == 321:
                url = message.content
                try:
                    requests.post(url, allow_redirects=False)
                except requests.exceptions.InvalidSchema:
                    pass
                except Exception as e:
                    #: TODO 网络异常处理
                    print(e)
    elif data.type == DECRYPT_IMAGE:
        # for message in data.message:
        #     md5 = message.wxid1
        #     content = message.content
        #     with open(f"C:/Users/Administrator/Desktop/wechat_robot/data/image_cache/{md5}.jpg", "wb") as wf:
        #         content = base64.b64decode(content)
        #         wf.write(content)
        #     print("-" * 10, f"{md5}.jpg", "-" * 10)
        pass


spy = WeChatSpy(parser=my_proto_parser, key="3ea954244f76a8cfb7e5f8f544cf6878", logger=logger)


def send(wxid: str, content: str):
    if content is not None and len(content) >= 1000:
        content = content[:999]
    if content:
        spy.send_text(wxid, content)


def send_file(wxid: str, file_path: str):
    spy.send_file(wxid, file_path)


def send_file_list_txt():
    send_file(GROUP_ID[0], os.path.join(DIR_PATH, '文件列表.txt'))


def send_msg_when(wxid: str, content: str, send_time: str):
    """
    定时发送微信消息
    :param wxid: 对方的wxid
    :param content: 内容
    :param send_time: 形如'2020-08-07 17:17:10' ‘%Y-%m-%d %H:%M’的时间
    """
    do_at_sometime(lambda: send(wxid, content), send_time)


def log_in():
    spy.run(r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe")
    logger.info('start receiving wechat message')
    while True:
        input()


def add_new_remark(wechat_id):
    spy.get_contact_details(wechat_id, update=True)


def image_decode(dat_path, dat_name):
    global xor_value
    # dat_dir_path, dat_name = os.path.split(dat_path)[0], os.path.split(dat_path)[1]
    # target_path = r'F:\Users\Tencent Files\WeChat Files\image'
    try:
        target_path = FILE_DIR_PATH
        with open(dat_path, "rb") as dat_read:
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            out = target_path + "\\" + dat_name + ".png"
            with open(out, "wb") as png_write:
                for now in dat_read:
                    for nowByte in now:
                        newByte = nowByte ^ xor_value
                        png_write.write(bytes([newByte]))
        return True
    except Exception as e:
        print(e)
        return False



if __name__ == '__main__':
    log_in()
