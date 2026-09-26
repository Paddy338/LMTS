'''
===============================================================================================================================
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. 
If not, see <https://www.gnu.org/licenses/>.
===============================================================================================================================
'''
# 依赖项：程序中的“关于”对话框 & 版本信息

import ttkbootstrap as ttk
import webbrowser
VERSION = '1.5.3'

def show_about():
    top = ttk.Toplevel(title = "关于")
    top.minsize(300, 300)
    top.maxsize(1000, 1000)
    text = ttk.Label(top, text = f'''局域网信息传输系统 (LMTS)
版本 {VERSION}
原作者：韩邦泽
二次开发：裴启迪''',)
    text.pack(padx = 20, pady = 20)

    link_frame1 = ttk.Labelframe(top, text = "原作者链接")
    link1_1 = ttk.Button(link_frame1,
                       bootstyle = 'link',
                       text = "官方网站",
                       command = lambda: webbrowser.open("https://hanbangze.tech/",0))
    link1_1.pack(padx=5, pady=5, side="top")
    link1_2 = ttk.Button(link_frame1,
                       bootstyle = 'link',
                       text = "仓库地址 (GitHub)",
                       command = lambda: webbrowser.open("https://github.com/hbzsoft/lan_message_transmission_system",0))
    link1_2.pack(padx = 5, pady= 5 ,side = "bottom")
    link_frame1.pack(padx = 20, pady = 20, side = "left")

    link_frame2 = ttk.Labelframe(top, text = "二次开发者链接")
    link2_1 = ttk.Button(link_frame2,
                       bootstyle = 'link',
                       text = "仓库地址 (Gitee)",
                       command = lambda: webbrowser.open("https://gitee.com/Paddy338/LMTS",0))
    link2_1.pack(padx = 5, pady = 5,side="top")
    link2_2 = ttk.Button(link_frame2,
                       bootstyle = 'link',
                       text = "仓库地址 (GitHub)",
                       command = lambda: webbrowser.open("https://github.com/Paddy338/LMTS",0))
    link2_2.pack(padx = 5, pady = 5,side = "bottom")
    link_frame2.pack(padx = 20, pady = 20, side = "right")

    top.mainloop()