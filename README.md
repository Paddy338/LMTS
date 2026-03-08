# 📌 基于原项目的二次开发说明

**本项目基于 [hbzsoft/lan_message_transmission_system](https://github.com/hbzsoft/lan_message_transmission_system) 进行二次开发。**

原项目作者：[@hbzsoft](https://github.com/hbzsoft)  
原项目许可证：GNU GPLv3

感谢原作者的优秀工作。

不知为何，我没找到发送端 v1.3 的源代码，就扒出了 v1.2 版本的并加了些额外的功能。  
现在找到了但就维持现状吧，我不想再对比。

少量逻辑为AI所写，但经过严格的检验。

# 已实现的功能
- 加急
- 现代化界面
- 常用IP地址

# 📖 正在开发的功能
- 批量发送信息
- 将接收到的消息插入新文本文档

# ⌨️ 功能、开发环境等
该项目允许用户通过局域网向接收端发布用弹窗显示的通知。  
弹窗置顶，并可能播放提示音。

运行环境：`Windows+Python 3.5` 以上或 `Ubuntu 20.04`以上  
需用 `pip` 安装 `pyperclip` 和 `ttkbootstrap`。

当前稳定版本：v1.4.0
当前预览版本：v1.5.0