# -*- coding: utf-8 -*-

from .modules import tk


class Text(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = None
        self.y_scrollbar = tk.Scrollbar(
            master=self.master, 
            orient="vertical",
            command=self.yview
        )
        self.y_scrollbar.pack(side="right", fill="y")
        self.x_scrollbar = tk.Scrollbar(
            master=self.master, 
            orient="horizontal",
            command=self.xview
        )
        self.x_scrollbar.pack(side="bottom", fill="x")
        self.configure(
            yscrollcommand=self.y_scrollbar.set,
            xscrollcommand=self.x_scrollbar.set,
            wrap="none",
            state="disabled",
            bg=self.master["bg"]
        )
        self.bind("<Button-3>", self.open_menu)
        self.bind("<Button-1>", lambda event: self.close_menu())
        
    def close_menu(self):
        if self.menu:
            self.menu.destroy()
            self.menu = None
        
    def open_menu(self, event):
        self.close_menu()
        self.menu = tk.Menu(master=None, tearoff=False)
        self.menu.add_command(
            label="Copy",
            command=lambda: self.focus_get().event_generate('<<Copy>>')
        )
        self.menu.add_command(
            label="Select All",
            command=lambda: self.focus_get().event_generate('<<SelectAll>>')
        )
        self.menu.post(event.x_root, event.y_root)
