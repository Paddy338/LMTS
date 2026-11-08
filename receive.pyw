# -----------------------------------------------------------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as 
# published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. 
# If not, see <https://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------------------------------------------------------

import queue
import socket
import sys
import threading
import time
import tkinter.messagebox as tkmsgbox
import tkinter.filedialog as filedialog
import webbrowser
from tkinter import *

import pyperclip
import ttkbootstrap as ttk
from utils import *

class LMTSServer:
    def __init__(self, root_win):
        self.PORT = 12345
        self.count = {} # 记录每个 IP 的最后发送时间（时间戳）
        self.msg_queue = queue.Queue()
        self.current_msg = ''
        self.root = root_win

        try:
            self.s = socket.socket(type = socket.SOCK_DGRAM)
            self.s.bind(('0.0.0.0',self.PORT))
        except OSError as err:
            tkmsgbox.showerror(title = "接收端 - 网络错误",
                message = f'''无法建立Socket，请检查本程序的另一实例是否还在运行。\n{err}''')
            exit(0)

    def urgent_beep(self):
        if sys.platform == "win32":
            import winsound
            try:
                winsound.PlaySound("assets/beep_1000hz.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception:
                winsound.Beep(1000, 1000)
        else:
            try:
                from playsound import playsound
                threading.Thread(
                    target=playsound,
                    args=("assets/beep_1000hz.wav",),
                    daemon=True
                ).start()
            except Exception as e:
                print(f"播放声音失败: {e}")

    def break_down(self, s):
        """处理消息：
        - 判断是否加急（末尾 \\a）
        - 如果没有换行符，每 30 字符自动换行
        """
        if not s:
            return
        if s[-1] == '\a':
            self.urgent_beep()
            s = s[:-1] # 移除末尾的 \a

        if s.find('\n'):
            return s
        else:
            return '\n'.join([s[i:i+30] for i in range(0, len(s), 30)])

    def open_url(self):
        """打开官方网站"""
        webbrowser.open('https://hanbangze.tech/', new = 0)


    def msg_saveas(self, parent_window, msg_str):
        path: str = filedialog.asksaveasfilename(
            parent = parent_window,
            title = "接收端 - 另存消息",
            defaultextension = ".txt",
            filetypes = [
                ("文本文档 (*.txt)", ".txt"),
                ("所有文件 (*.*)", "")
            ],
        )
        if not path:
            return False
        try:
            with open(path, "w", encoding="utf-8-sig") as f:
                f.write(msg_str)
                return True
        except Exception as e:
            return False
    

    def show_message(self, text, addr):
        """显示从 addr 接收到的消息 `text` 的弹窗。
        此函数仅在 GUI 线程上运行。"""
        
        self.current_msg = text
        msg_local = text # 局部变量，处理复制、另存等事宜
        if not text:
            return
        
        t = time.localtime()
        received_time = f'''接收时间：{t.tm_year}/{t.tm_mon}/{t.tm_mday} {t.tm_hour}:{t.tm_min:02d}\
:{t.tm_sec:02d}''' # 分秒补零防止出现类似 0:0:0 的情况

        window = ttk.Toplevel(self.root) # 使用深色主题
        window.wm_attributes("-topmost", 1)
        window.title(f'''局域网信息传输系统 (LMTS) v{VERSION} - 接收端''')
        load_window_icon(window)


        message = ttk.Text(window, font = ("Noto Sans SC", 30))
        message.configure(width = 25, height = 8)
        message.insert('1.0', self.break_down(text))
        message.tag_configure("center", justify = "center")
        message.tag_add("center", "1.0", 'end')
        message.config(state = DISABLED) # 只读模式：用 Text 模拟 Label
        message.pack(padx = 2, pady = 2, expand = TRUE, fill = BOTH)
    
        frm_addr = ttk.Label(window, text = f'由 {addr[0]} 发送')
        frm_addr.pack()

        btn_frame = ttk.Frame(window)
        btn_frame.pack()
        copy_btn = ttk.Button(btn_frame, text = '复制', command = lambda: pyperclip.copy(msg_local), width = 4)
        copy_btn.pack(padx = 5, pady = 5, side = "left")
        saveas_btn = ttk.Button(btn_frame, text = '另存...', 
            command = lambda: self.msg_saveas(window, msg_local.replace('\a', '')), 
            width = 4, bootstyle="secondary")
        saveas_btn.pack(padx=5, pady=5, side = "right")

        recv_time_label = ttk.Label(window, text = received_time, foreground="#808080")
        recv_time_label.pack()

        
        toolbar = ttk.Frame(window)
        toolbar.pack(side = "bottom", fill = "x")
        
        about_btn = ttk.Button(toolbar, text = "关于", command = show_about, bootstyle = "outline")
        about_btn.pack(side = "right", padx = 4, pady = 4)


        website = ttk.Label(toolbar,
                        text = '官方网站: hanbangze.tech',
                        font = ("Arial",8),
                        foreground="#808080")
        website.pack(side = "left", padx = 4)

    def process_queue(self):
        """处理消息队列（从监听线程`listener()`传来的消息）\\
            定时看有没有新消息，有就弹窗口"""
        try:
            text, addr = self.msg_queue.get_nowait()
        except queue.Empty:
            return
        self.show_message(text, addr)


    def listener(self): 
        """监听线程：接收 UDP 消息并放入队列"""
        while True:
            data, addr = self.s.recvfrom(2048)
            ip = addr[0]
            cnt = self.count.get(ip)
            if cnt is None:
                self.count[ip] = int(time.time())
            else:
                diff = int(time.time()) - cnt
                if diff <= 5:
                    self.s.sendto(b'refused', addr)
                    continue
                else:
                    self.count[ip] = int(time.time())
            try:
                msg = data.decode('gbk')
            except UnicodeDecodeError:
                continue
            self.s.sendto(b'received', addr)
            self.msg_queue.put((msg, addr))
            self.root.after(0, self.process_queue)

def main():
    """主函数：精简程序入口（`if __name__ == "__main__"`）处代码"""
    # 创建一个不可见根窗口用于事件循环
    root = ttk.Window(themename = "darkly")
    root.withdraw()
    server = LMTSServer(root_win = root)

    # 启动接收线程
    th = threading.Thread(target = server.listener, daemon = True)
    th.start()

    root.mainloop()

if __name__ == "__main__":
    main()
    