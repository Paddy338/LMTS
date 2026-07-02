'''
====================================================================================================
Modified by Pei Qidi in 2025
====================================================================================================
This program is free software: you can redistribute it and/or modify it under the terms of the GNU 
General Public License as published by the Free Software Foundation, either version 3 of the License, 
or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without 
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. 
If not, see <https://www.gnu.org/licenses/>.
====================================================================================================
'''

from tkinter import *
import tkinter.messagebox as tkmsgbox
import tkinter.font as tkfont
import socket
import webbrowser
import json

import ttkbootstrap as ttk
from show_about import VERSION, show_about

# 初始化变量、常量
IP_FILE = "ips.json"
MESSAGE_TYPEFACE_FAMILY = "Courier"
MESSAGE_TEXT_SIZE = 12
global msg, ip, urgent


def open_url(url):
    webbrowser.open(url, new = 0)

def send_socket():
    s=socket.socket(type = socket.SOCK_DGRAM)
    s.settimeout(1)
    s.bind(("0.0.0.0",14514))
    message = msg.get("1.0","end-1c")
    if urgent.get():
        message += "\a"
    s.sendto(message.encode("gbk"), (ip_entry.get(), 12345))
    try:
        (c,addr) = s.recvfrom(1024)
    except ConnectionResetError as err:
        tkmsgbox.showerror(title = "错误",
                             message = f'''网络错误\n详细信息：{err}''')
    except socket.timeout as err:
        tkmsgbox.showerror(title = "错误",
                             message = f'''网络错误\n详细信息：{err}''')
    else:
        if c.decode() == "received":
            tkmsgbox.showinfo(title = "提示",
                                message = "接受端收到了您的信息。")
        elif c.decode() == "refused":
            tkmsgbox.showerror(title="提示",
                                 message = "发送太频繁，请稍后重试。")


# 选择一个主题并创建窗口
window = ttk.Window(themename = "cosmo")
window.title("局域网信息传输系统 (LMTS) v%s - 发送端" % VERSION)
try:
    window.iconbitmap("icons/appicon.ico")
except TclError:
    try:
        window.iconbitmap("appicon.ico")
    except TclError:
        window.iconbitmap("")
        tkmsgbox.showinfo(message="加载应用图标错误，将回退到默认图标。")

ip_var = ttk.StringVar()   # 选中的 IP 地址

# 工具栏
toolbar = ttk.Frame(window, bootstyle = "light")
toolbar.pack(side = "top", fill = "x")
try:
    info_icon = ttk.PhotoImage(file = "icons/about.png")
    info_btn = ttk.Button(toolbar, image = info_icon, command = show_about, bootstyle = "link")
except:
    info_btn = ttk.Button(toolbar, text = "关于", command = show_about, bootstyle = "link")
info_btn.pack(side = "right", padx = 5)


# 输入IP地址
ipaddr_form = ttk.Labelframe(window, padding = 10, text = "目标 IP 地址")
ipaddr_form.pack(side = LEFT, fill = Y, padx = 10, pady = 10)


def load_ip_list():
    global ip_list
    try:
        with open(IP_FILE, 'r', encoding = 'utf-8') as file:
            ip_list = json.load(file)
            if not isinstance(ip_list,list): # 判断ip_list是不是列表类型
                ip_list = []
    except json.JSONDecodeError:
        tkmsgbox.showwarning(title = "JSON 解析错误", message = "JSON 文件的字符串格式不正确，可能是擅自不正确地修改了 JSON 文件。\n 将把常用 IP 地址置为空状态。")
        ip_list = []
    except FileNotFoundError:
        # 文件可能还未创建
        ip_list = []

def save_ip_list():
    with open(IP_FILE, 'w', encoding = 'utf-8') as file:
        json.dump(ip_list, file, ensure_ascii = False, indent = 4)

ip_entry_frame = ttk.Frame(ipaddr_form)
ip_entry_frame.pack(pady = 5)


load_ip_list()
ip_entry = ttk.Combobox(ip_entry_frame, values = ip_list, width = 20, cursor = "ibeam")
ip_entry.pack(side = LEFT, padx = 5)

def add_ip():
    new_ip = ip_entry.get().strip()
    if new_ip and new_ip not in ip_list:
        ip_list.append(new_ip)
        save_ip_list()
        ip_entry["values"] = ip_list

add_button = ttk.Button(ip_entry_frame, text = "添加", command = add_ip, bootstyle = "secondary")
add_button.pack(side=RIGHT)

input_hint_str = "在输入框中输入 IP 地址。\n点击“添加”将其加入下拉选项常用列表。"
input_hint = ttk.Label(ipaddr_form, text=input_hint_str)
input_hint.pack(padx = 5, pady = 5)

# 输入信息
default_font = tkfont.Font(family = MESSAGE_TYPEFACE_FAMILY,
                            size = MESSAGE_TEXT_SIZE)
msg = ttk.Text(window, width = 80, height = 25, font = default_font)
msg.pack(padx = 5, pady = 5, fill = BOTH, expand = True)

urgent_frm = ttk.Frame(window)
urgent_frm.pack()
urgent = ttk.BooleanVar()
urgent_check = ttk.Checkbutton(urgent_frm,
                                text="加急（接收端将发出提示音）",
                                variable=urgent)
urgent_check.pack()

send = ttk.Button(window,
                    text="发送",
                    command=send_socket,
                    bootstyle="primary",
                    width=5)
send.pack(pady=8)

link = ttk.Label(window,
                    text="官方网站: hbzsoft.github.io",
                    font=("Arial",8))
link.pack()

window.mainloop()
