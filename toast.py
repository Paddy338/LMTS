'''
InnerToast v0.1：在 Ttkbootstrap 窗口内显示 Toast。(buggy)

# 已实现功能
- 自定义图标
- 定时自动消失
- 成功、警告、错误等 bootstyle

# 用法示例（片段）
```python
toast = Toast(root)
toast.show_toast("test message")
'''
import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.icons import *

class Toast:
    def __init__(self, parent: ttk.Window | ttk.Toplevel):
        self.parent = parent
        self._timer_id = None

        self.root_frame = ttk.Frame(parent) # 根容器，供以后多条toast扩充
        self.content_frame = ttk.Frame(self.root_frame, padding=(12, 8))
        self.content_frame.pack()
        self.content_frame.columnconfigure(0, weight=0)
        self.content_frame.columnconfigure(1, weight=1)

        # 预加载几个ttkbootstrap图标
        self.icon_default = tk.PhotoImage(data=Icon.info, master=self.parent)
        self.icon_info = tk.PhotoImage(data=Icon.info, master=self.parent)
        self.icon_warning = tk.PhotoImage(data=Icon.warning, master=self.parent)
        self.icon_error = tk.PhotoImage(data=Icon.error, master=self.parent)

        

    def show_toast(self, 
        message: str,
        duration = 3000, # 单位：毫秒
        bootstyle: str = "light",
        ico: str = None
    ):
        self.message = message
        self.bootstyle = bootstyle
        self.duration = duration

        self.loaded_icon: tk.Photoimage
        if ico is None:
            self.loaded_icon = self.icon_default
        elif "info" in ico:
            self.loaded_icon = self.icon_info
        elif "warning" in ico:
            self.loaded_icon = self.icon_warning
        elif "error" in ico:
            self.loaded_icon = self.icon_error
        else:
            self.loaded_icon = self.icon_default

        if self._timer_id:
            self.parent.after_cancel(self._timer_id)

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.content_frame.configure(bootstyle=bootstyle)

        self.icon_lbl = ttk.Label(
            self.content_frame,
            anchor=CENTER,
            bootstyle=f"inverse-{self.bootstyle}")
        self.icon_lbl.grid(row=0, column=0, sticky=NSEW, padx=(4, 2))

        if "success" in ico:
            self.icon_lbl.configure(text = Emoji.get("WHITE HEAVY CHECK MARK")) # 对勾 Emoji
        else:
            self.icon_lbl.configure(image = self.loaded_icon)
            self.icon_lbl.image = self.loaded_icon

        self.message_lbl = ttk.Label(
            self.content_frame,
            anchor=NW,
            text=self.message,
            bootstyle=f"inverse-{self.bootstyle}")
        self.message_lbl.grid(row=0, column=1, sticky=NSEW, pady=4, padx=(2, 4))

        self.root_frame.place(relx=0.98, rely=0.95, anchor="se")
        self.root_frame.lift()
        self._timer_id = self.parent.after(duration, self.hide_toast)

    def hide_toast(self):
        self.root_frame.place_forget()
        self._timer_id = None

if __name__ == "__main__":
    root = ttk.Window()
    root.geometry("600x400")
    root.title("窗口内 Toast 测试")
    toast = Toast(parent=root)

    btn1 = ttk.Button(root, text = "Toast (primary)", 
        command=lambda: toast.show_toast(
            message="测试消息",
            bootstyle="primary",
            ico = "info"))
    btn1.pack(padx=8, pady=8)

    btn2 = ttk.Button(root, text = "Toast (success)", 
        command=lambda: toast.show_toast(
            message="测试消息",
            bootstyle="success",
            ico = "success"),
        bootstyle="success")
    btn2.pack(padx=8, pady=8)

    btn3 = ttk.Button(root, text = "Toast (warning)", 
        command=lambda: toast.show_toast(
            message="测试消息",
            bootstyle="warning",
            ico = "warning"),
        bootstyle="warning")
    btn3.pack(padx=8, pady=8)

    btn4 = ttk.Button(root, text = "Toast (error)", 
        command=lambda: toast.show_toast(
            message="测试消息",
            bootstyle="danger",
            ico = "error"),
        bootstyle="danger")
    btn4.pack(padx=8, pady=8)

    root.mainloop()