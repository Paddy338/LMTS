'''
====================================================================================================
Modified by Pei Qidi in 2026
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
import json

import ttkbootstrap as ttk
from show_about import VERSION, show_about

LOAD_OK = 0
RESTORED_BAK = 1
LOAD_EMPTY = 2

class IPListManager:
    '''
    加载、处理 IP 地址文件（目前仅支持数组格式 `/ips.json`）
    '''
    def __init__(self, file_path: str, bak_path: str):
        self.file = file_path
        self.bak_file = bak_path
        self.ip_data = []
        self.load_ip_list()

    def load_ip_list(self) -> int:
        try:
            with open(self.file, 'r', encoding = 'utf-8') as f:
                self.ip_data = json.load(f)
                return LOAD_OK
                if not isinstance(self.ip_data, list):
                    self.ip_data = []
                    return LOAD_EMPTY

        except FileNotFoundError: # ips.json 未创建或已删除
            self.ip_data = []
            return LOAD_EMPTY
        
        except json.JSONDecodeError: # ips.json 被篡改，解码错误
            try:
                with open(self.bak_file, 'r', encoding = "utf-8") as f:
                    self.ip_data = json.load(f)
                if isinstance(self.ip_data, list):
                    with open(self.file, 'w', encoding="utf-8") as recv_file:
                        json.dump(self.ip_data, recv_file)
                        return RESTORED_BAK
            except (json.JSONDecodeError, FileNotFoundError):
                self.ip_data = []
                return LOAD_EMPTY


    def save_ip_list(self):
        with open(self.file, 'w', encoding = 'utf-8') as f:
            json.dump(self.ip_data, f, ensure_ascii = False, indent = 4)
        with open(self.bak_file, "w", encoding = "utf-8") as f:
            json.dump(self.ip_data, f, ensure_ascii = False, indent = 4)

    def get_all_ip(self) -> list:
        return self.ip_data.copy()

class UDPNetwork:
    '''
    处理 Socket 和消息发送
    '''
    def __init__(self, REMOTE_PORT = 12345):
        self.local_port = 14514
        self.remote_port = REMOTE_PORT
        self.s=socket.socket(type = socket.SOCK_DGRAM)
        self.s.settimeout(1)
        self.s.bind(("0.0.0.0", self.local_port))

    def send_socket(self, dest_ip: str, msg: str):
        '''
        `dest_ip`: 目标 IP 地址。  
        `msg`: 要发送的消息。

        发送完之后结果是返回值，不是消息弹窗。
        '''
        self.s.sendto(msg.encode("gbk"), (dest_ip, self.remote_port))

        try:
            (status, _addr)=self.s.recvfrom(1024)
            return status.decode()
        except ConnectionResetError:
            return "connectionreset"
        except socket.timeout:
            return "timeout"

'''
========================================== UI ==========================================
'''
class MainWindow:
    def __init__(self, root: ttk.Window, ip_list: IPListManager, network: UDPNetwork):
        self.root = root # 主窗口
        self.iplistmgr = ip_list
        self.net = network

        self.msg_input = None # 消息输入框
        self.urgent = ttk.BooleanVar() # 加急状态
        self.ip_combobox = None

        self.root.title(f'''局域网信息传输系统 (LMTS) v{VERSION} - 发送端''')
        try:
            self.root.iconbitmap("icons/appicon.ico")
        except TclError:
            try:
                self.root.iconbitmap("appicon.ico")
            except TclError:
                self.root.iconbitmap("")
                tkmsgbox.showinfo(message = "加载应用图标错误，将回退到默认图标。")

        self.render_ui()

    def render_ui(self):
        '''
        网格布局：
        | 地址区 | 信息区 |
        |    状态栏（横跨整行）      | 
        '''
        self.root.grid_rowconfigure(0, weight = 1)
        self.root.grid_rowconfigure(1, weight = 0)
        self.root.grid_columnconfigure(0, weight = 0)
        self.root.grid_columnconfigure(1, weight = 1)

        # IP 地址
        self.ipaddr_form = ttk.Labelframe(self.root, padding = 10, text = "目标 IP 地址")
        self.ipaddr_form.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "nsew")
        self.ip_entry_frame = ttk.Frame(self.ipaddr_form)
        self.ip_entry_frame.pack(pady = 5)
        self.ip_combobox = ttk.Combobox(self.ip_entry_frame, width = 20, cursor = "xterm")
        self.ip_combobox["values"] = self.iplistmgr.get_all_ip()
        self.ip_combobox.pack(side = LEFT, padx = 5)
        self.add_button = ttk.Button(self.ip_entry_frame, text = "添加",
                                     command = self.add_new_ip, bootstyle = "secondary")
        self.add_button.pack(side = RIGHT)

        self.input_hint_str = "在输入框中输入 IP 地址。\n点击“添加”将其固定至下拉选项。"
        self.input_hint = ttk.Label(self.ipaddr_form, text = self.input_hint_str)
        self.input_hint.pack(pady = 5)

        # 输入消息
        self.msg_frm = ttk.Frame(self.root, padding = 10)
        self.msg_frm.grid(row = 0, column = 1, padx = 10, sticky = "nsew")
        default_font = tkfont.Font(family = "Courier", size = 12)
        self.msg_input = ttk.Text(self.msg_frm, width = 80, height = 25, 
                                    font = default_font, cursor = "xterm")
        self.msg_input.pack(padx = 5, pady = 5, fill = BOTH, expand = True)

        self.urgent_frm = ttk.Frame(self.msg_frm)
        self.urgent_frm.pack()
        self.urgent_check = ttk.Checkbutton(self.urgent_frm,
                                        text = "加急（接收端将播放提示音）",
                                        variable = self.urgent)
        self.urgent_check.pack()

        self.send_btn = ttk.Button(self.msg_frm, text = "发送", command = self.do_send,
                            bootstyle = "primary", width = 5)
        self.send_btn.pack(pady=8)

        # 状态栏：官方网站文字和相关操作按钮
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.grid(row = 1, column = 0, columnspan = 2, 
                            stick = "ew", padx = 2, pady = 2)
        self.website = ttk.Label(self.status_bar, text = "官方网站: hanbangze.tech",
                            font = ("Arial", 8), bootstyle = "secondary")
        self.website.pack(side = "left")

        try:
            self.about_icon = ttk.PhotoImage(file = "icons/about.png")
            self.about_btn = ttk.Button(self.status_bar, image = self.about_icon, command = show_about, bootstyle = "link")
        except:
            self.about_btn = ttk.Button(self.status_bar, text = "关于", command = show_about, bootstyle = "link")
        self.about_btn.pack(side = "right", padx = 5)

    def add_new_ip(self):
        ip = self.ip_combobox.get().strip()
        ip_list = self.iplistmgr.ip_data
        if ip and ip not in ip_list:
            ip_list.append(ip)
            self.iplistmgr.ip_data = ip_list
            self.iplistmgr.save_ip_list()
        self.ip_combobox["values"] = self.iplistmgr.get_all_ip()
        self.ip_combobox.delete(0, "end")

    def do_send(self):
        target_ip = self.ip_combobox.get()
        msg_content = self.msg_input.get("1.0", "end").strip()
        if self.urgent.get():
            msg_content += "\a"

        result = self.net.send_socket(dest_ip = target_ip, msg = msg_content)
        if result == "received":
            tkmsgbox.showinfo(title = "提示",
                                message = "接受端收到了您的信息。")
        elif result == "refused":
            tkmsgbox.showwarning(title="警告",
                                message = "发送太频繁，请稍后重试。")
        elif result == "timeout":
            tkmsgbox.showerror(title = "错误",
                                message = '''网络错误：连接超时。\n请检查 IP 地址是否正确、对端电脑是否已开启接收端、网络是否畅通。''')
        elif result == "connectionreset":
            tkmsgbox.showerror(title = "错误",
                                message = '''网络错误：连接已重置。\n请检查 IP 地址是否正确、对端电脑是否已开启接收端、网络是否畅通。''')
        
if __name__=="__main__":
    iplist = IPListManager(file_path = "ips.json", bak_path = "ips.bak")
    network = UDPNetwork()

    window = ttk.Window(themename = "cosmo")
    app = MainWindow(window, iplist, network)
    window.mainloop()