# wechat_file_arranger
由于微信没有群文件，使用该程序管理某个群的群文件(已考虑了潜在的多群开发需求，可围绕列表GROUP_ID进行相关自定义)

以下情况视作添加文件
1. 管理员发送文件给机器人账号
2. 目标群中任意成员发送的文件

有以下功能：
1. 群成员发送'文件列表'、 '文件'、 '查询'或 '查询文件'时，机器人会在群里发送当前已保存的文件列表
2. 发送文件对应的编号时，机器人会在群里发送对应文件
