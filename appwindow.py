import tkinter as tk
from tkinter import ttk


class AppWindow():
    E = tk.E
    W = tk.W
    N = tk.N
    S = tk.S
    NS = N + S
    EW = E + W
    NEWS = tk.N + tk.E + tk.W + tk.S

    SUN_VALLEY_PATH = "/home/sid/pycodes/gui/THEMES/Sun-Valley/sun-valley.tcl"
    BREEZE_PATH = "/home/sid/pycodes/gui/THEMES/breeze/breeze.tcl"


    def __init__(self, title:str='', size:str='640x480', theme:str = None, cleanup_func = None) -> None:
        '''Boilerplate code to create a root app window.
        Arguments: Window Title, Window Size, Theme (sun-valley or breeze), Cleanup Function
        '''
        self.root = tk.Tk()
        self.root.wm_title(title)
        self.root.wm_resizable(0,0)
        self.root.wm_geometry(size)
        
        if theme != None:
            self.set_theme(theme)

        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)

        self.frame0 = ttk.Frame(self.root,padding=5)
        self.frame0.grid(row=0,column=0,sticky=self.NEWS)

        # intercept the window close event
        self.root.protocol('WM_DELETE_WINDOW',lambda:self.root_close(cleanup_func))
        
    def show(self):
        '''Shows the application window and starts the mainloop.'''
        self.root.mainloop()
    
    def set_icon(self,appicon:tk.PhotoImage):
        if appicon != None:
            self.root.tk.call('wm', 'iconphoto', self.root._w, appicon)
    
    def set_theme(self, theme:str):
        if theme == 'sun-valley':
            self.root.tk.call("source", self.SUN_VALLEY_PATH )
            self.root.tk.call("set_theme", "light")
        elif theme == 'breeze':
            self.root.tk.call("source", self.BREEZE_PATH)
            style = ttk.Style(self.root)
            style.theme_use('breeze')

    def root_close(self, cleanup_func = None) -> None:
        '''Do some cleanup actions before the main window is closed. The second parameter is a function that has some cleanup code.
        '''
        if cleanup_func != None:
            try:
                cleanup_func()
            except Exception as e:
                raise e
            finally:
                self.root.destroy()
        else:
            self.root.destroy()
  