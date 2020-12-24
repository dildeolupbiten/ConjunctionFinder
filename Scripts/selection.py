# -*- coding: utf-8 -*-

from .modules import tk
from .constants import PLANETS, SIGNS


class Selection(tk.Frame):
    def __init__(self, text, objects, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(bd=1, relief="sunken")
        self.label = tk.Label(
            master=self, 
            text=text, 
            font="Default 12 bold"
        )
        self.label.pack()
        self.widgets = {}
        self.create_widgets(objects)

    def create_widgets(self, objects):
        pass
        
        
class CheckbuttonSelection(Selection):
    def __init__(self, text, objects, *args, **kwargs):
        super().__init__(
            text=text, 
            objects=objects,
            *args, 
            **kwargs
        )
        
    def create_widgets(self, objects):
        frame = tk.Frame(master=self)
        frame.pack()
        for index, obj in enumerate(["Select/Unselect All"] + [*objects]):
            label = tk.Label(master=frame, text=obj)
            label.grid(row=index, column=0, sticky="w")
            var = tk.BooleanVar()
            var.set(False)
            checkbutton = tk.Checkbutton(master=frame, variable=var)
            checkbutton.grid(row=index, column=1)
            self.widgets[obj] = [var, checkbutton]
        self.widgets["Select/Unselect All"][1]["command"] = \
            self.select_unselect_all
    
    def select_unselect_all(self):
        if self.widgets["Select/Unselect All"][0].get():
            for v in self.widgets.values():
                v[0].set(True)
        else:
            for v in self.widgets.values():
                v[0].set(False)
        
        
class EntrySelection(Selection):
    def __init__(self, text, objects, *args, **kwargs):
        super().__init__(
            text=text, 
            objects=objects,
            *args, 
            **kwargs
        ) 
        
    def create_widgets(self, objects):
        frame = tk.Frame(master=self)
        frame.pack()
        for index, obj in enumerate(objects):
            label = tk.Label(master=frame, text=obj)
            label.grid(row=0, column=index)
            entry = tk.Entry(master=frame, width=6)
            entry.grid(row=1, column=index)
            self.widgets[obj] = [entry]


class PlanetSelection(CheckbuttonSelection):
    def __init__(self, *args, **kwargs):
        super().__init__(
            text="Select Planets",
            objects=PLANETS,
            *args,
            **kwargs
        )
        
        
class SignSelection(CheckbuttonSelection):
    def __init__(self, *args, **kwargs):
        super().__init__(
            text="Select Signs",
            objects=SIGNS,
            *args,
            **kwargs
        )
        
        
class YearRangeSelection(EntrySelection):
    def __init__(self, *args, **kwargs):
        super().__init__(
            text="Select Year Range", 
            objects=["From", "To"],
            *args, 
            **kwargs
        )
        
        
class OrbSelection(EntrySelection):
    def __init__(self, *args, **kwargs):
        super().__init__(
            text="Select Orb Factor", 
            objects=["Orb"],
            *args, 
            **kwargs
        )    
