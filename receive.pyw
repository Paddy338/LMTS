'''
Modified by Pei Qidi in 2025

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.'''

from tkinter import *
import tkinter.messagebox as tkmsgbox
import socket
import threading
import time
import webbrowser
import winsound
import queue

import pyperclip
import ttkbootstrap as ttk
from show_about import VERSION, show_about

PORT=12345
try:
    s=socket.socket(type=socket.SOCK_DGRAM)
    s.bind(('0.0.0.0',PORT))
except OSError as err:
    tkmsgbox.showerror(title="错误",message=f'''无法建立Socket，请检查本程序的另一实例是否还在运行。\n{err}''')
count={}
c=''
msg=''
msg_queue = queue.Queue()
current_msg = ''

def break_down(s):
    """处理消息：
    判断是否加急（末尾 \\a），自动换行"""
    if not s:
        return
    if s[-1]=='\a':
        winsound.Beep(1000, 1000)
        x=''
        for i in range(len(s)-1):
            x+=s[i]
        s=x
        if s.find('\n'):
            return s
        else:
            return '\n'.join([s[i:i+30] for i in range(0, len(s), 30)])
    if s.find('\n'):
        return s
    else:
        return '\n'.join([s[i:i+30] for i in range(0, len(s), 30)])

def open_url():
    """打开官方网站"""
    webbrowser.open('https://hbzsoft.github.io/',new=0)

def cp():
    """将最后显示的消息复制到剪贴板"""
    pyperclip.copy(current_msg)

def show_message(text, addr):
    """显示从 addr 接收到的消息 `text` 的弹窗。
    此函数仅在 GUI 线程上运行。"""
    
    global current_msg
    current_msg = text
    if not text:
        return
    
    window = ttk.Window()
    window.config(background='black')
    window.wm_attributes('-topmost', True)
    window.title('局域网信息传输系统 (LMTS) v%s - 接收端' % VERSION)
    try:
        window.iconbitmap("icons/appicon.ico")
    except TclError:
        try:
            window.iconbitmap("appicon.ico")
        except TclError:
            window.iconbitmap("")


    menubar = ttk.Menu(window)
    window.config(menu=menubar)

    main_menu = ttk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='菜单', menu=main_menu)
    main_menu.add_command(label='关于...', command=show_about)


    label = Text(window, font=("Noto Sans SC", 30))
    label.configure(foreground='white', background='black', width=25, height=8)
    label.insert('1.0', break_down(text))
    label.tag_configure("center", justify="center")
    label.tag_add("center", "1.0", 'end')
    label.config(state=DISABLED) # 只读模式
    label.pack(padx=2, pady=2, expand=TRUE, fill=X)
  
    frm_addr = ttk.Label(window, text='由 ' + addr[0] + ' 发送')
    frm_addr.configure(foreground='white', background='black')
    frm_addr.pack()
    copy = Button(window, text='复制', command=cp)
    copy.pack(padx=5, pady=5)

    link = ttk.Label(window,
                    text='官方网站: hbzsoft.github.io',
                    font=("Arial",8))
    link.configure(foreground="white", background="black", borderwidth=0)
    link.pack()

# 以下是 Python 网络编程的稳定写法
def process_queue():
    """处理消息队列（从监听线程传来的消息）\\
        定时看有没有新消息，有就弹窗口"""
    try:
        text, addr = msg_queue.get_nowait()
    except queue.Empty:
        return
    show_message(text, addr)


def listener(): 
    """监听线程：接收 UDP 消息并放入队列"""
    while True: # 无限循环监听
        data, addr = s.recvfrom(2048) # 收消息
        ip = addr[0]
        cnt = count.get(ip)
        if cnt is None:
            count[ip] = int(time.time())
        else:
            diff = int(time.time()) - cnt
            if diff <= 5: # 防刷屏，5 秒内不能重复发
                s.sendto(b'refused', addr)
                continue
            else:
                count[ip] = int(time.time())
        msg = data.decode('gbk')
        s.sendto(b'received', addr)
        msg_queue.put((msg, addr))
        root.after(0, process_queue)

##################################################

# 创建一个不可见根窗口用于事件循环
root = Tk()
root.withdraw()

# 启动接收线程
th = threading.Thread(target=listener, daemon=True)
th.start()

root.mainloop()
