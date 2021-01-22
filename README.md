# wechat_file_arranger
由于微信没有群文件且聊天文件很容易过期，使用Django+PyWechatSpy管理**单个群**的群文件(本说明中称其为目标群)



## 背景：

1. 有**一个**目标群，群成员活跃，每日消息量很大，群文件查阅不便
2. 微信文件容易过期，且目标群内的文件有较长时间后查询的需求
3. 项目开发者有一个闲置微信号



## 功能及使用说明：

### 1. 如何获得使用权限：

+ 在目标群中曾发过言且被机器人检测到过
+ 向机器人账户私聊发送“激活”

### 2. 文件上传

#### 如何上传文件：

##### ①如果您是**普通群成员** :

+ 当您向机器人发送图片或文件时，这些图片/文件将会被视为群文件并上传
+ 您可以向机器人发送“``上传``”，来获取上传文件的网址，文件大小上限为50M
+ 上传过程中，机器人会提示您输入该文件的备注，有以下几种情形：
  1. 如果您想要上传的**仅是一个**文件/图片
     + 如果该文件的名称已足以说明其属性，无需备注，请在机器人提示您输入文件备注时，向程序发送空格“ ”或“``取消``”
     + 如果该文件的名称不足以说明其属性，需要备注，请在机器人提示您输入文件备注时，向程序发送该文件的备注，如“``01-22会议记录``”
  2. 如果您想要上传的是**多个**文件/图片
     + 如果想要给这些文件有**不同的备注**，请按照单一文件处理
     + 如果想要给这些文件有**相同的备注**，您可以在机器人提示您输入文件备注时，继续向机器人发送文件/图片，（但请不要发送文字，否则程序将会将其当作文件的备注）。当所有待上传文件发送完成后，发送备注文字即可完成上传。

##### ②如果您是**管理员** (管理员账户需要在后台添加wx_id) :

+ 您可以向机器人发送“``管理``”，来获取管理后台的网址，随后登录以管理数据库
+ 其余操作与普通群成员操作相同

### 3. 文件查看

1. 在目标群中的群成员可以直接发送“``文件``”或“``文件列表``”来获取文件列表网址，查询的文件将会发送到群里。
2. 已激活使用权限的群成员可以**私聊**机器人发送“``文件``”或“``文件列表``”来获取文件列表网址，查询的文件将会是与您私聊。



## 使用时的注意事项:

1. 进入上传、查询网址时均需验证密钥，且每次获取的密钥仅有**10分钟有效期**，以保证文件安全性，故请在需要查看文件时即时获取。
2. 如果会遇上网络不佳的情况或文件较大，发送时耗时会相对延长，还请耐心等待。



## 克隆注意事项:

1. 本项目是根据实际情况定制而成，局限性较大，克隆时仅供参考
2. 使用前请先从GitHub上[克隆PyWechatSpy](https://github.com/veikai/PyWeChatSpy)。微信相关的功能实现须感谢@[veikai](https://github.com/veikai)开发的sdk
3. wechat_func中，为保证端口不冲突，程序启动后会生成名为occupy的文件，请在下一次启动时将其删除
4. 可选功能：微信掉线时发送警告邮件，需要在.\util\message_config.ini填写相关参数
5. 机器号电脑端发送的所有信息都会失效
6. 为保证本项目的安全，含有本项目密钥的setting、secret_code文件并未上传，setting为django的setting文件，secret_code文件的同名函数请另行封装
7. 迁移的指令请参考django的migrate相关指令
8. 项目代码中网址为yx.loange.top，请将其修改可用的url



## 其他说明

如果遇到业务调整，本项目不得不停运之时，所有保存的群文件将会交由负责主管另行保管。

本项目代码开源，欢迎交流。

2021-01-22