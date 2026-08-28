> [旧版 README](https://github.com/Paddy338/LMTS/blob/main/archive/README_old.md) （或打开仓库内的 archive/README_old.md 文件。）

![GitHub Tag](https://img.shields.io/github/v/tag/Paddy338/LMTS)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/Paddy338/LMTS/total)
![GitHub repo size](https://img.shields.io/github/repo-size/Paddy338/LMTS)
![GitHub Last Commit](https://img.shields.io/github/last-commit/Paddy338/LMTS?logo=github)

![GitHub Repo stars](https://img.shields.io/github/stars/Paddy338/LMTS)


# 💬 项目简介
局域网信息传输系统 (LMTS) 是一个轻量级的**局域网通知工具**，
可以在校园、实验室等局域网环境下，向指定电脑发送弹窗消息。

尤其适合电教委员、老师向全班同学发布通知提醒，或学校内部电脑间基础纯文本通信。

## ✨ 功能
- 简单可靠——基于 UDP 协议，接收端固定监听端口，无需额外服务器。
- **醒目的弹窗**——消息以大字体、置顶窗口显示，并标明发送者 IP。
- **加急**——勾选“加急”后，接收端会响铃（Windows）。（v1.3+）
- 发送频率限制——同一个 IP 地址 5 秒内只能发送一次消息，防止刷屏。
- 一键复制——接收者点击“复制”按钮即可将消息内容复制到剪贴板。

## 正在规划或开发的功能
- [ ] **(短)** 将接收到的消息另存为文本文档
    - 时间戳、源 IP、消息内容等
- [ ] **(中)** 实现窗口内嵌入式 Toast 提示
    - 借鉴 ttkbootstrap 2.x；非屏幕全局提示
- [ ] **(调研)** 代码在低版本 Python (3.6/3.7) 的兼容性、打包后在 Windows 7 的兼容性
- [ ] **(中)** 深色模式自动切换 & 手动覆盖
- [ ] **(中)** 给不同的 IP 地址群发信息
- [ ] **(中)** 更详尽的主题切换
- [ ] **(长)** 接收端任务栏图标

# 💻 使用方法
1. 在本仓库 Releases (发行版) 下载打包版。
2. 下载或克隆仓库（必要文件和目录：根目录的 `.pyw` 文件、`/icons/`），安装依赖库运行源码。

> 环境要求请见项目 Wiki 「使用前须知」。

# 🙏 致谢与贡献者
- **原作者**：韩邦泽（[hbzsoft](https://github.com/hbzsoft) | 南京外国语学校 2022 级初中毕业生，现就读于西安交通大学）  
    - 开发了 v1.0 ~ v1.3 版本，完成基础框架。  
    - [原仓库地址](https://github.com/hbzsoft/lan_message_transmission_system)

- **二次开发者**：裴启迪（[Paddy338](https://github.com/Paddy338) | 南京外国语学校 2025 级初中学生）

感谢原作者的贡献。
> [!NOTE]
> 关于 AI 使用：部分代码或逻辑为 AI 所提供，但经过严格的检验以避免出错。

# 许可证
本程序是自由软件：你可以根据自由软件基金会发布的 GNU 通用公共许可证 第 3 版（或更高版本）的条款，重新分发和/或修改它。

详情请见 [COPYING](https://github.com/Paddy338/LMTS/blob/main/COPYING) 文件。