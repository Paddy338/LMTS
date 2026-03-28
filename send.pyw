'''
Modified by Pei Qidi in 2025

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.'''

from tkinter import *
import tkinter.messagebox as tkmsgbox
import tkinter.font as tkfont
import ttkbootstrap as ttk
import socket
import webbrowser
import json
# 初始化变量
VERSION='1.5.0'
IP_FILE='ips.json'
message_typeface_family="Courier"
message_text_size=12
radio_buttons = []         # 存储 Radiobutton 控件，方便刷新
global msg, ip, urgent

def show_about():
    tkmsgbox.showinfo(title='关于', message='''局域网信息传输系统 (LMTS) 
版本 %s
原作者：韩邦泽
二次开发：裴启迪
'''%VERSION)

def open_url(URL):
    webbrowser.open(URL,new=0)

def send_socket():
    s=socket.socket(type=socket.SOCK_DGRAM)
    s.settimeout(1)
    s.bind(('0.0.0.0',14514))
    message = msg.get('1.0','end-1c')
    if urgent.get():
        message += '\a'
    s.sendto(message.encode('gbk'),(ip_var.get(),12345))
    try:
        (c,addr)=s.recvfrom(1024)
    except ConnectionResetError:
        tkmsgbox.showerror(title='错误',
                             message='网络错误/接收端未运行\n详细信息：ConnectionResetError\n连接已重置。')
    except socket.timeout:
        tkmsgbox.showerror(title='错误',
                             message='网络错误/接收端未运行\n详细信息：响应时间太长。')
    else:
        if c.decode()=='received':
            tkmsgbox.showinfo(title='提示',
                                message='接受端收到了您的信息。')
        elif c.decode()=='refused':
            tkmsgbox.showerror(title='提示',
                                 message='发送太频繁，请稍后重试。')

'''
def main():
    # 创建窗口及组件
    global msg, ip, urgent
    windows=Tk()
    try:
        windows.iconbitmap("icons/appicon.ico") # 运行时记得从当前目录启动
    except TclError:
        try:
            windows.iconbitmap("appicon.ico")
        except TclError:
            windows.iconbitmap("")  # 回退到默认图标
            tkmsgbox.showinfo(message='加载应用图标错误，可能自定义图标不在当前目录。\n将回退到默认图标。')

    # 菜单
    menubar = Menu(windows)
    windows.config(menu=menubar)

    # 文件菜单
    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="文件", menu=file_menu)
    file_menu.add_command(label="退出", command=windows.quit)

    # 帮助菜单
    help_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="帮助", menu=help_menu)
    help_menu.add_command(label="仓库地址", command=lambda: open_url('https://github.com/Paddy338/LMTS'))
    help_menu.add_command(label="官方网站", command=lambda: open_url('https://hbzsoft.github.io/'))
    help_menu.add_separator()

    help_menu.add_command(label="关于...", command=show_about)

    ipaddr_frm=Frame(windows)
    ipaddr_frm.pack()
    ip_hint=Label(ipaddr_frm,text='接收端 IP 地址: ')
    ip_hint.pack(side='left')
    ip=Entry(ipaddr_frm) # IP 地址输入框
    ip.pack(side='right')
    windows.title('局域网信息传输系统 (LMTS) v%s - 发送端'%VERSION)

    default_font = tkfont.Font(family=message_typeface_current_family, size=message_text_size)
    msg=Text(windows,width=100,height=20,font=default_font) # 信息输入框
    msg.pack()

    urgent_frm=Frame(windows) # 加急
    urgent_frm.pack()
    urgent=BooleanVar()
    urgent_check=Checkbutton(urgent_frm,text='加急（接收端将发出提示音）',variable=urgent)
    urgent_check.pack()

    send=Button(windows,text='发送',command=send_socket,font=('Microsoft Yahei UI',14),background="#1890FF") # 发送按钮
    send.pack()

    link = Button(windows, text='官方网站: hbzsoft.github.io', font=('Arial,宋体', 8),command=lambda: open_url('https://hbzsoft.github.io/'),borderwidth=0)
    link.pack()
    windows.mainloop()'''


# 先选择一个主题并创建窗口
windows = ttk.Window(themename='cosmo')
windows.title('局域网信息传输系统 (LMTS) v%s - 发送端' % VERSION)
try:
    windows.iconbitmap("icons/appicon.ico")
except TclError:
    try:
        windows.iconbitmap("appicon.ico")
    except TclError:
        windows.iconbitmap("")
        tkmsgbox.showinfo(message='加载应用图标错误，可能自定义图标不在当前目录。\n将回退到默认图标。')

ip_var = ttk.StringVar()   # 选中的 IP 地址
# 菜单
menubar = Menu(windows)
windows.config(menu=menubar)

file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="文件", menu=file_menu)
file_menu.add_command(label="退出", command=windows.quit)

help_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="帮助", menu=help_menu)
help_menu.add_command(label="仓库地址",
                        command=lambda: open_url('https://github.com/Paddy338/LMTS'))
help_menu.add_command(label="官方网站",
                        command=lambda: open_url('https://hbzsoft.github.io/'))
help_menu.add_separator()
help_menu.add_command(label="关于...", command=show_about)

# 输入IP地址
'''ipaddr_frm = ttk.Frame(windows)
ipaddr_frm.pack()
ip_hint = ttk.Label(ipaddr_frm, text='接收端 IP 地址: ')
ip_hint.pack(side='left')
ip = ttk.Entry(ipaddr_frm)
ip.pack(side='right')'''
ipaddr_form=ttk.Frame(windows)
ipaddr_form.pack(side=LEFT, fill=Y, padx=10, pady=10)

ip_hint=ttk.Label(ipaddr_form, text="IP 地址：")
ip_hint.pack(anchor=W)
ip_entry=ttk.Entry(ipaddr_form)
ip_entry.pack(anchor=W)

def load_ip_list():
    global ip_list
    try:
        with open(IP_FILE, 'r', encoding='utf-8') as file:
            ip_list=json.load(file)
            if not isinstance(ip_list,list): # 判断ip_list是不是列表类型
                ip_list=[]
    except (FileNotFoundError, json.JSONDecodeError):
        ip_list=[]

def save_ip_list():
    with open(IP_FILE, 'w', encoding='utf-8') as file:
        json.dump(ip_list, file, ensure_ascii=False, indent=4)

def refresh_ip_list():
    # 清空旧控件
    for rb in radio_buttons:
        rb.destroy()
    radio_buttons.clear()

    # 重新生成单选框
    for ip in ip_list:
        rb = ttk.Radiobutton(ipaddr_form, text=ip, value=ip, variable=ip_var)
        rb.pack(anchor=W)
        radio_buttons.append(rb)

def add_ip():
    new_ip = ip_entry.get().strip()
    if new_ip and new_ip not in ip_list:
        ip_list.append(new_ip)
        save_ip_list()
        refresh_ip_list()
        ip_entry.delete(0, 'end') # 清空输入框

load_ip_list()
refresh_ip_list()
if ip_list:
    ip_var.set(ip_list[0])
else:
    ip_var.set('')
ttk.Button(ipaddr_form, text="添加", command=add_ip).pack(anchor=W,pady=10)

# 输入信息
default_font = tkfont.Font(family=message_typeface_family,
                            size=message_text_size)
msg = Text(windows, width=100, height=20, font=default_font)
msg.pack()

urgent_frm = ttk.Frame(windows)
urgent_frm.pack()
urgent = ttk.BooleanVar()
urgent_check = ttk.Checkbutton(urgent_frm,
                                text='加急（接收端将发出提示音）',
                                variable=urgent)
urgent_check.pack()

send = ttk.Button(windows,
                    text='发送',
                    command=send_socket,
                    bootstyle='primary',
                    width=5,
                    )
send.pack()

link = ttk.Button(windows,
                    text='官方网站: hbzsoft.github.io',
                    bootstyle='link',
                    command=lambda: open_url('https://hbzsoft.github.io/'))
link.pack()

windows.mainloop()
