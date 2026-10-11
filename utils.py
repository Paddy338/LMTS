'''
一些共用依赖项：版本号、关于对话框等
'''
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

import ttkbootstrap as ttk
import webbrowser
import sys
VERSION = '1.5.4'

def show_about():
    top = ttk.Toplevel(title = "关于")
    top.minsize(300, 300)
    top.maxsize(1000, 1000)
    text = ttk.Label(top, text = f'''局域网信息传输系统 (LMTS)
版本 {VERSION}
原作者：韩邦泽（hbzsoft）
二次开发：裴启迪（Paddy338）''',)
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

def load_window_icon(root: ttk.Window | ttk.Toplevel):
    ico_path = "assets/appicon.ico"
    png_path = "assets/appicon.png"

    if sys.platform == "win32":
        # Windows：优先 ICO，任务栏、Alt‑Tab渲染正常
        try:
            root.iconbitmap(str(ico_path))
            return
        except Exception as e:
            # 兜底：PNG iconphoto
            try:
                # 挂载到root实例防止GC回收
                root._appicon = ttk.PhotoImage(file=str(png_path))
                root.iconphoto(True, root._tk_app_icon)
            except Exception as e2:
                pass

    else:
        try:
            root._appicon = PhotoImage(file=str(png_path))
            root.iconphoto(True, root._tk_app_icon)
        except Exception as e:
            pass