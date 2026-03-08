'''
Modified by Pei Qidi in 2025

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.'''

from tkinter import *
import tkinter.messagebox as tkmsgbox
import pyperclip
import re
import socket
import threading
import time
import ttkbootstrap as ttk
import webbrowser
import winsound
import queue

VERSION='1.5.0'
port=12345
try:
    s=socket.socket(type=socket.SOCK_DGRAM)
    s.bind(('0.0.0.0',port))
except OSError as err:
    tkmsgbox.showerror(title="错误",message=f'''无法建立Socket，有可能本程序的另一实例还在运行。\n{err}''')
count={}
c=''
msg=''
label_font_western="Times New Roman"
label_font_cn="仿宋"

# queue for passing messages from listener thread to GUI thread
msg_queue = queue.Queue()
# most recent message shown (for clipboard copy)
current_msg = ''
##################################################
def get_ip():
    try:
        tempsocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tempsocket.connect(('1.1.1.1', 80))
        ip=tempsocket.getsockname()[0]
        tempsocket.close()
        return ip
    except:
        return '获取失败，可能未连接 Internet。\n 你可以在命令提示符中输入 ipconfig /all 查看 IP 地址。'
def show_about():
    tkmsgbox.showinfo(title='关于', message='''局域网信息传输系统 (LMTS) 
版本 %s
原作者：韩邦泽
二次开发：裴启迪
'''%VERSION)
def break_down(s):
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
    webbrowser.open('https://hbzsoft.github.io/',new=0)
def cp():
    """Copy the last-displayed message to the clipboard."""
    pyperclip.copy(current_msg)
'''def show():
    if not msg:
        return
    
    root = Tk()
    # 设置窗口属性
    root.config(bg='black')
    root.wm_attributes('-topmost', True)
    try:
        root.iconbitmap("icons/appicon.ico") # 运行时记得从当前目录启动
    except TclError:
        try:
            root.iconbitmap("appicon.ico")
        except TclError:
            root.iconbitmap("")  # 回退到默认图标
            tkmsgbox.showinfo(message='加载应用图标错误，可能自定义图标不在当前目录。\n将回退到默认图标。')

    root.title('局域网信息传输系统 (LMTS) v%s - 接收端'%VERSION)
    
    # 向窗口添加组件
    menubar=Menu(root)
    root.config(menu=menubar)

    file_menu=Menu(menubar,tearoff=0)
    menubar.add_cascade(label='文件', menu=file_menu)
    file_menu.add_command(label='复制消息', command=cp)
    file_menu.add_command(label='退出', command=root.quit)

    help_menu=Menu(menubar,tearoff=0)
    menubar.add_cascade(label='帮助',menu=help_menu)
    help_menu.add_command(label='官方网站', command=open_url)
    help_menu.add_command(label='关于', command=show_about)

    label = Text(root, font=(label_font_western,30),fg='white',bg='black',width=25,height=10)
    label.insert('1.0',break_down(msg))
    label.tag_configure("center",justify="center")
    label.tag_add("center","1.0",'end')
    label.config(state=DISABLED)
    s = label.get("1.0", "end-1c")
    for m in re.finditer(r'[\u4e00-\u9fff]+', s):
        start = "1.0 + %d chars" % m.start()
        end = "1.0 + %d chars" % m.end()
        label.tag_add("cn", start, end)
    label.tag_configure("cn", font=label_font_cn)
    label.pack()
    
    frm_addr=Label(root,text='由  '+addr[0]+' 发送',fg='white',bg='black')
    frm_addr.pack()
    copy = Button(root,font=('Microsoft Yahei UI',14),text='复制',command=cp,background="#1890FF")
    copy.pack()
    
    link = Button(root, text='官方网站: hbzsoft.github.io', font=('Arial', 8),command=open_url,fg="white",bg="black",borderwidth=0)
    
    link.pack()
    root.mainloop()'''
def show_message(text, addr):
    """Display a popup window for *text* received from *addr*.
    This function runs on the GUI thread only.
    """
    global current_msg
    current_msg = text
    if not text:
        return
    win = ttk.Toplevel()
    # 设置窗口属性
    win.config(bg='black')
    win.wm_attributes('-topmost', True)
    try:
        win.iconbitmap("icons/appicon.ico")
    except TclError:
        try:
            win.iconbitmap("appicon.ico")
        except TclError:
            win.iconbitmap("")
            # tkmsgbox.showinfo(message='加载应用图标错误，可能自定义图标不在当前目录。\n将回退到默认图标。')

    win.title('局域网信息传输系统 (LMTS) v%s - 接收端' % VERSION)

    menubar = Menu(win)
    win.config(menu=menubar)

    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='文件', menu=file_menu)
    file_menu.add_command(label='复制消息', command=cp)
    file_menu.add_command(label='退出', command=win.destroy)

    help_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='帮助', menu=help_menu)
    help_menu.add_command(label='官方网站', command=open_url)
    help_menu.add_command(label='关于', command=show_about)

    label = Text(win, font=(label_font_western, 30))
    label.configure(foreground='white', background='black',
                    width=25, height=10) # 显式设置属性防止主题覆盖
    label.insert('1.0', break_down(text))
    label.tag_configure("center", justify="center")
    label.tag_add("center", "1.0", 'end')
    label.config(state=DISABLED)
    s = label.get("1.0", "end-1c")
    for m in re.finditer(r'[\u4e00-\u9fff]+', s):
        start = "1.0 + %d chars" % m.start()
        end = "1.0 + %d chars" % m.end()
        label.tag_add("cn", start, end)
    label.tag_configure("cn", font=label_font_cn)
    label.pack()

    frm_addr = Label(win, text='由  ' + addr[0] + ' 发送')
    frm_addr.configure(foreground='white', background='black')
    frm_addr.pack()
    copy = Button(win, font=('Microsoft Yahei UI', 14), text='复制', command=cp)
    copy.pack()

    link = Button(win, text='官方网站: hbzsoft.github.io', font=('Arial', 8),
                  command=open_url)
    link.configure(fg="white", bg="black", borderwidth=0)
    link.pack()


def process_queue():
    try:
        text, addr = msg_queue.get_nowait()
    except queue.Empty:
        return
    show_message(text, addr)


def listener(): # 监听线程
    while True:
        data, addr = s.recvfrom(2048)
        ip = addr[0]
        cnt = count.get(ip)
        if cnt is None:
            count[ip] = int(time.time())
        else:
            diff = int(time.time()) - cnt
            if diff <= 5:
                s.sendto(b'refused', addr)
                continue
            else:
                count[ip] = int(time.time())
        msg = data.decode('gbk')
        s.sendto(b'received', addr)
        msg_queue.put((msg, addr))
        root.after(0, process_queue)

##################################################
local_ip = get_ip()
tkmsgbox.showinfo(title='启动信息', message=f'''接收端已启动
端口：{port}，IP地址：{local_ip}
如果在错误消息弹出后看到本对话框，则接收端未正常启动。''')

# 创建一个不可见根窗口用于事件循环
root = ttk.Window(themename="cosmo")
root.withdraw()

# 启动接收线程
th = threading.Thread(target=listener, daemon=True)
th.start()

root.mainloop()
