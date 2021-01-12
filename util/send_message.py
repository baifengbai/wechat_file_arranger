import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

from configparser import ConfigParser

message_config = ConfigParser()
message_config_path = 'util\\message_config.ini'
message_config.read(message_config_path, encoding='utf-8')
message_config.get('main', 'my_sender')

my_sender = message_config.get('main', 'my_sender')  # 发件人邮箱账号
my_pass = message_config.get('main', 'my_pass')  # 发件人邮箱stmp授权码
my_user = message_config.get('main', 'my_user')  # 收件人邮箱账号
post = int(message_config.get('main', 'post'))
stmp_service = message_config.get('main', 'service')


def mail():
    ret = True
    try:
        msg = MIMEText('Warning！微信机器人连接丢失', 'plain', 'utf-8')
        msg['From'] = formataddr(("laorange", my_sender))  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(("管理员", my_user))  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "微信机器人连接丢失"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL(stmp_service, post)  # 发件人邮箱中的SMTP服务器
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


def send_mail():
    ret = mail()
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")


if __name__ == '__main__':
    send_mail()
