# wechat_file_arranger
由于微信没有群文件，使用该程序管理某个群的群文件(已考虑了潜在的多群开发需求，可围绕列表GROUP_ID进行相关自定义)

以下情况视作添加文件
1. 管理员发送文件给机器人账号
2. 目标群中任意成员发送的文件

有以下功能：
1. 群成员发送 '文件列表'、'文件'、'查询' 或 '查询文件'时，机器人会在群里发送当前已保存的文件列表
2. 发送文件对应的编号时，机器人会在群里发送对应文件

注意事项:
1. 使用前请先从GitHub上[克隆微信机器人的库](https://github.com/veikai/PyWeChatSpy) 
2. 可选功能：微信掉线时发送警告邮件，需要在.\util\message_config.ini填写相关参数
3. 可选功能：管理员可向机器人发送图片来将其添加到文件列表中，如需使用该功能，请参考 [如何解密微信图片](https://blog.csdn.net/zhanglw882/article/details/110221075) 来配置xor_value
4. 机器号电脑端发送的所有信息都会失效
5. 为增加可靠性，系统收到文件后，10秒后才会开始后续操作