# -*- coding: utf-8 -*-

from .modules import tk
from .utilities import create_image_files


class MsgBox(tk.Toplevel):
    msgbox = []

    def __init__(
            self, 
            title, 
            message, 
            level, 
            width=350, 
            height=100,
    ):
        super().__init__()
        for i in self.msgbox:
            i.destroy()
        self.geometry(f"{width}x{height}")
        self.title(title)
        self.resizable(width=False, height=False)
        self.icons = create_image_files("Icons")
        self.level_icon = self.icons[level]["img"]
        self.frame = tk.Frame(master=self)
        self.frame.pack(expand=True, fill="both")
        self.icon_label = tk.Label(
            master=self.frame,
            image=self.level_icon,
        )
        self.icon_label.pack(side="left", expand=True, fill="both")
        self.message_label = tk.Label(
            master=self.frame,
            text=message,
            font="Arial 14 bold",
            anchor="w"
        )
        self.message_label.pack(side="left", expand=True, fill="both")
        self.button_frame = tk.Frame(master=self)
        self.button_frame.pack(side="bottom")
        self.button = tk.Button(
            master=self.button_frame,
            text="OK",
            command=self.destroy,
        )
        self.button.pack(side="bottom")
        self.msgbox.append(self)
        self.wait_window()
