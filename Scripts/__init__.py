# -*- coding: utf-8 -*-

from .modules import tk
from .main_window import MainWindow
            

def main():
    root = tk.Tk()
    root.resizable(width=False, height=False)
    root.title("ConjunctionFinder")
    MainWindow(master=root)
    root.mainloop()
