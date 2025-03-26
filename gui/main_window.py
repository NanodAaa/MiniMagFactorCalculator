# main_windows.py

from functions.MinMagFactor.gui import min_mag_factor_window as mafw
import tkinter as tk

class MainWindow(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self._init_gui()
        self._start()
        
    def _init_gui(self):
        self.title('CMSSim')
        
        # Menu
        self.menu = tk.Menu(self)
        
        # Menu-Tools
        self.tools_menu = tk.Menu(self.menu, tearoff=False)
        self.tools_menu.add_command(label='MinMagFactor Calculator', command=self._onclick_menu_tools_min_mag_factor_calculator)
        self.menu.add_cascade(label='Tools', menu=self.tools_menu)
        
        self.config(menu=self.menu)
        
    def _start(self):
        self.mainloop()
        return
    
    def _onclick_menu_tools_min_mag_factor_calculator(self):
        min_mag_factor_window = mafw.MinMagFactorWindow(self)
        
        return