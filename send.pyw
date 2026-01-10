'''
Modified by Pei Qidi in 2025

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.'''

import socket
from tkinter import *
from tkinter import messagebox
import webbrowser
VERSION='1.4'
message_typeface='Courier'
message_textsize=12
def show_about():
    messagebox.showinfo(title='关于', message='''局域网信息传输系统 (LMTS) 
版本 %s
原作者：韩邦泽
二次开发：裴启迪
'''%VERSION)
def open_url():
    webbrowser.open('https://hbzsoft.github.io/',new=0)
def custom_font():
    dialog_box=Toplevel()
    dialog_box.title('字体')
    dialog_box.geometry('300x150')
    font_family=Label(master=dialog_box,text='字体族：')
    font_family.pack()
    font_family_input=Text(dialog_box,width=30,height=1)
    font_family_input.insert('1.0', message_typeface)

    font_family_input.pack()

    font_size=Label(master=dialog_box,text='字号：')
    font_size.pack()
    font_size_input=Text(master=dialog_box,width=10,height=1)
    font_size_input.insert('1.0', message_textsize)
    font_size_input.pack()
    def apply_font():
        global message_typeface, message_textsize
        new_family = font_family_input.get('1.0','end-1c').strip() or message_typeface
        try:
            new_size_text = font_size_input.get('1.0','end-1c').strip()
        except NameError:
            new_size_text = str(message_textsize)
        try:
            new_size = int(new_size_text) if new_size_text else message_textsize
        except ValueError or new_size > 100 or new_size < 6:
            messagebox.showerror(title='错误', message='字号必须为整数，介于6和100之间。')
            return
        message_typeface = new_family
        message_textsize = new_size
        try:
            msg.configure(font=(message_typeface, message_textsize))
        except NameError:
            pass
        dialog_box.destroy()

    apply_btn = Button(dialog_box, text='确定', command=apply_font)
    apply_btn.pack()
def send_socket():
    s=socket.socket(type=socket.SOCK_DGRAM)
    s.settimeout(1)
    s.bind(('0.0.0.0',14514))
    message = msg.get('1.0','end-1c')
    if urgent.get():
        message += '\a'
    s.sendto(message.encode('gbk'),(ip.get(),12345))
    try:
        (c,addr)=s.recvfrom(1024)
    except ConnectionResetError:
        messagebox.showerror(title='局域网信息传输系统 (LMTS) 提示：',
                             message='网络错误/接收端未运行\n连接已重置。')
    except socket.timeout:
        messagebox.showerror(title='局域网信息传输系统 (LMTS) 提示：',
                             message='网络错误/接收端未运行\n响应时间太长。')
    else:
        if c.decode()=='received':
            messagebox.showinfo(title='局域网信息传输系统 (LMTS) 提示：',
                                message='接收端收到了您的信息。')
        elif c.decode()=='refused':
            messagebox.showerror(title='局域网信息传输系统 (LMTS) 提示：',
                                 message='发送太频繁，请稍后重试。')

# 创建窗口及组件
windows=Tk()
# 菜单
menubar = Menu(windows)
windows.config(menu=menubar)

# 文件菜单
file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="文件", menu=file_menu)
file_menu.add_command(label="字体...", command=custom_font)
file_menu.add_command(label="退出", command=windows.quit)

# 帮助菜单
help_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="帮助", menu=help_menu)
help_menu.add_command(label="官方网站", command=open_url)
help_menu.add_separator()

help_menu.add_command(label="关于...", command=show_about)

ipaddr_frm=Frame(windows)
ipaddr_frm.pack()
ip_hint=Label(ipaddr_frm,text='接收端 IP 地址: ')
ip_hint.pack(side='left')
ip=Entry(ipaddr_frm) # IP 地址输入框
ip.pack(side='right')
windows.title('局域网信息传输系统 (LMTS) v%s by Bangze Han'%VERSION)

msg=Text(windows,width=100,height=20,font=(message_typeface,message_textsize)) # 信息输入框
msg.pack()

urgent_frm=Frame(windows) # 加急
urgent_frm.pack()
urgent=BooleanVar()
urgent_check=Checkbutton(urgent_frm,text='加急（接收端将发出提示音）',variable=urgent)
urgent_check.pack()

send=Button(windows,text='发送',command=send_socket,width=10,height=2,font=('Microsoft Yahei UI',14)) # 发送按钮
send.pack()

link = Button(windows, text='官方网站: hbzsoft.github.io', font=('Arial,宋体', 8),command=open_url,borderwidth=0)
link.pack()
mainloop()
