#!/bin/env python3

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from appwindow import AppWindow
from icons import ICONS64
import get_comics as gc
from PIL import ImageTk, Image
from pathlib import Path
# import imghdr
from io import BytesIO
import random

ICONS = {}


class Dilbert():
    def __init__(self) -> None:
        self.app = AppWindow(size='1400x600',title='Dilbert')
        self.app.set_theme('sun-valley')
        # self.app.set_theme('breeze')

        ICONS['APP'] = tk.PhotoImage(data=ICONS64['APP'])
        ICONS['BACK'] = tk.PhotoImage(data=ICONS64['BACK'])
        ICONS['FOWARDS'] = tk.PhotoImage(data=ICONS64['FORWARD'])
        ICONS['EXIT'] = tk.PhotoImage(data=ICONS64['EXIT'])
        ICONS['SAVE'] = tk.PhotoImage(data=ICONS64['SAVE'])
        ICONS['SYNC'] = tk.PhotoImage(data=ICONS64['SYNC'])
        ICONS['RAND'] = tk.PhotoImage(data=ICONS64['RAND'])


        self.app.set_icon(ICONS['APP'])

        self.make_layout()
        self.app.show()

    def __del__(self):
        gc.con.close()

    def make_layout(self):
        self.frame0 = self.app.frame0
        frame0 = self.frame0

        frame0.columnconfigure(0,weight=0)
        frame0.columnconfigure(1,weight=1)
        frame0.rowconfigure(0,weight=0)
        frame0.rowconfigure(1,weight=1)
        frame0.rowconfigure(2,weight=0)

        # hframe = ttk.Frame(frame0)
        # hframe.grid(row=0,column=1,columnspan=1)
        # ttk.Label(hframe,text='Dilbert',font='sans 16 bold').grid(row=0,column=0,sticky=AppWindow.NEWS)
        self.frame1()
        self.frame2()
        self.frame3()
        self.frame4()

        self.fill_years()
        self.fill_months()
        self.fill_bookmarks()
        self.fill_dates()
        self.show_comic(self.lst_date.get(self.lst_date.curselection()))
        self.app.root.bind('<Key-b>',lambda x: self.toggle_bookmark())
        self.app.root.bind('<Key-r>',lambda x: self.get_random())

    def frame1(self):
        app = self.app
        frame1 = tk.Frame(app.frame0)
        frame1.grid(row=0,column=0,sticky=AppWindow.NEWS,padx=5, rowspan=2)
        frame1.rowconfigure(0,weight=1)
        frame1.columnconfigure(0,weight=1)

        self.nb = ttk.Notebook(frame1)
        self.nb.grid(row=0,column=0,sticky=AppWindow.NEWS)

        # Frame 1_1
        frame1_1 = ttk.Frame(self.nb)
        frame1_1.grid(row=0,column=0,sticky=AppWindow.NEWS)
        frame1_1.columnconfigure(0,weight=0)
        frame1_1.columnconfigure(1,weight=1)
        frame1_1.columnconfigure(2,weight=0)
        frame1_1.rowconfigure(0,weight=0)
        frame1_1.rowconfigure(1,weight=0)
        frame1_1.rowconfigure(2,weight=0)
        frame1_1.rowconfigure(3,weight=1)

        ttk.Label(frame1_1,text='Year').grid(row=0,column=0,sticky=AppWindow.W,padx=5,pady=5)
        ttk.Label(frame1_1,text='Month').grid(row=1,column=0,sticky=AppWindow.W,padx=5,pady=5)
        ttk.Label(frame1_1,text='Date').grid(row=2,column=0,sticky=AppWindow.W,padx=5,pady=5)

        self.cmb_year = ttk.Combobox(frame1_1)
        self.cmb_month = ttk.Combobox(frame1_1)
        self.cmb_year.grid(row=0,column=1,sticky=AppWindow.EW,padx=5,pady=5,columnspan=2)
        self.cmb_month.grid(row=1,column=1,sticky=AppWindow.EW,padx=5,pady=5,columnspan=2)

        self.lst_date = tk.Listbox(frame1_1,exportselection=False)
        self.lst_date.grid(row=3,column=0,columnspan=2,sticky=AppWindow.NEWS)
        srl_v = ttk.Scrollbar(frame1_1,orient='vertical',command=self.lst_date.yview)
        self.lst_date.configure(yscrollcommand=srl_v.set)
        srl_v.grid(row=3,column=2,sticky=AppWindow.NS + AppWindow.E)

        self.years = tk.StringVar()
        self.months = tk.StringVar()
        
        self.dates_ar = []
        self.dates = tk.StringVar(value = self.dates_ar)

        self.cmb_year.configure(textvariable=self.years)
        self.cmb_month.configure(textvariable=self.months)
        self.lst_date.configure(listvariable=self.dates)

        self.cmb_year.configure(state='readonly')
        self.cmb_month.configure(state='readonly')


        # Frame 1_2
        frame1_2 = ttk.Frame(self.nb)
        frame1_2.grid(row=0,column=0,sticky=AppWindow.NEWS)
        frame1_2.columnconfigure(0,weight=1)
        frame1_2.columnconfigure(1,weight=0)
        frame1_2.rowconfigure(0,weight=1)


        self.lst_bkmrk = tk.Listbox(frame1_2, exportselection=False)
        self.lst_bkmrk.grid(row=0,column=0,sticky=AppWindow.NEWS)
        srl_v2 = ttk.Scrollbar(frame1_2,orient='vertical',command=self.lst_bkmrk.yview)
        self.lst_bkmrk.configure(yscrollcommand=srl_v.set)
        srl_v2.grid(row=0,column=1,sticky=AppWindow.NEWS)

        self.bookmarks_arr = []
        self.bookmarks = tk.StringVar(value = self.bookmarks_arr)
        self.lst_bkmrk.configure(listvariable=self.bookmarks)

        # Set up notebook tabs
        self.nb.add(frame1_1,text='All')
        self.nb.add(frame1_2,text='Bookmarks')

        # bind events
        self.cmb_year.bind('<<ComboboxSelected>>',lambda x:self.fill_months())
        self.cmb_month.bind('<<ComboboxSelected>>',lambda x:self.fill_dates())
        self.lst_date.bind('<<ListboxSelect>>',lambda x:self.show_comic(self.lst_date.get(self.lst_date.curselection())))
        self.lst_bkmrk.bind('<<ListboxSelect>>',lambda x:self.show_comic(self.lst_bkmrk.get(self.lst_bkmrk.curselection())))

    def frame2(self):
        app = self.app
        frame2 = ttk.Frame(app.frame0)
        frame2.grid(row=0,column=1,sticky=AppWindow.NEWS,rowspan=2)
        frame2.columnconfigure(0,weight=1)
        frame2.columnconfigure(1,weight=0)
        frame2.rowconfigure(0,weight=1)
        frame2.rowconfigure(1,weight=0)
        
        self.cvs = tk.Canvas(frame2, background='white', scrollregion=(0, 0, 2000, 2000))
        self.cvs.grid(row=0,column=0,sticky=AppWindow.NEWS)

        srl_v = ttk.Scrollbar(frame2,orient='vertical',command=self.cvs.yview)
        self.cvs.configure(yscrollcommand=srl_v.set)
        srl_v.grid(row=0,column=1,sticky=AppWindow.NS)

        srl_h = ttk.Scrollbar(frame2,orient='horizontal',command=self.cvs.xview)
        self.cvs.configure(xscrollcommand=srl_h.set)
        srl_h.grid(row=1,column=0,sticky=AppWindow.EW)

    def frame3(self):
        app = self.app
        frame3 = ttk.Frame(app.frame0)
        frame3.grid(row=2, column=0, sticky=AppWindow.EW)
        frame3.columnconfigure(0, weight=1)
        frame3.columnconfigure(1, weight=1)
        frame3.columnconfigure(2, weight=1)
        frame3.columnconfigure(3, weight=1)
        frame3.rowconfigure(0, weight=1)

        btn_exit = ttk.Button(frame3,image=ICONS['EXIT'],command=lambda:app.root_close())
        btn_save = ttk.Button(frame3,image=ICONS['SAVE'],command=self.save_comic)
        btn_sync = ttk.Button(frame3,image=ICONS['SYNC'],command=self.sync)
        btn_rand = ttk.Button(frame3,image=ICONS['RAND'],command=self.get_random)

        btn_exit.grid(row=0, column=0, padx=5, pady=5, sticky=AppWindow.W)
        btn_sync.grid(row=0, column=1, padx=5, pady=5)
        btn_rand.grid(row=0, column=2, padx=5, pady=5)
        btn_save.grid(row=0, column=3, padx=5, pady=5, sticky=AppWindow.E)

        app.root.bind('<Key-Escape>',lambda x:btn_exit.invoke())

    def frame4(self):
        app = self.app
        frame4 = ttk.Frame(app.frame0)
        frame4.grid(row=2, column=1, sticky=AppWindow.EW)
        frame4.columnconfigure(0, weight=1)
        frame4.columnconfigure(1, weight=1)
        frame4.columnconfigure(2, weight=1)
        frame4.rowconfigure(0, weight=1)

        btn_back = ttk.Button(frame4,image=ICONS['BACK'], command=lambda:self.back())
        btn_forward = ttk.Button(frame4,image=ICONS['FOWARDS'], command=lambda:self.forward())

        btn_back.grid(row=0, column=0, padx=5, pady=5, sticky=AppWindow.W)
        btn_forward.grid(row=0, column=2, padx=5, pady=5, sticky=AppWindow.E)

        self.bkmrk = tk.BooleanVar()
        self.bkmrk.set(False)
        chk_bkmrk = ttk.Checkbutton(frame4,text='Bookmark',variable=self.bkmrk, onvalue=True, offvalue=False, command=self.set_bookmark)
        chk_bkmrk.grid(row=0, column=1, padx=5, pady=5)

        app.root.bind('<Key-Left>',lambda x:btn_back.invoke())
        app.root.bind('<Key-Right>',lambda x:btn_forward.invoke())

    def fill_years(self):
        self.years_arr = gc.get_years()
        self.cmb_year['values'] = self.years_arr
        if len(self.cmb_year['values']) > 0:
            self.cmb_year.current(len(self.cmb_year['values']) -1 )
            if len(self.cmb_month['values']) > 0:
                self.cmb_month.current(len(self.cmb_month['values']) -1 )

    def fill_months(self):
        self.months_arr = gc.get_months(self.years.get())
        self.cmb_month['values'] = self.months_arr
        if len(self.cmb_month['values']) > 0:
            self.cmb_month.current(len(self.cmb_month['values']) -1 )
            self.cmb_month.event_generate('<<ComboboxSelected>>')
    
    def fill_dates(self):
        self.dates_ar = gc.get_dates(self.years.get(),self.months.get())
        self.dates.set(self.dates_ar)
        self.lst_date.selection_clear(0,'end')
        self.lst_date.selection_set(len(self.dates_ar)-1,len(self.dates_ar)-1)
        self.lst_date.see(self.lst_date.curselection())
        self.lst_date.event_generate('<<ListboxSelect>>')

    def show_comic(self,date:str):
        try:
            self.comic_date = date
            url = gc.get_link(date)
            self.comic = gc.get_picture(url)
            self.img = ImageTk.PhotoImage(data = self.comic)
            self.cvs.create_image(0,0,image=self.img,anchor=AppWindow.N + AppWindow.W)
            
            buffer = BytesIO(self.comic)
            im = Image.open(buffer)
            self.imgtype = im.format
            # set the canvas scroll area same as the image
            self.cvs.configure(scrollregion=(0,0,im.width,im.height))

            if self.comic_date in self.bookmarks_arr:
                self.bkmrk.set(True)
            else:
                self.bkmrk.set(False)
        except Exception as e:
            messagebox.showerror('Error',f'Error while getting the comic for {date}. Error details are displayed below:\n\n{e}')
            self.cvs.delete('all')

    def back(self):
        if self.nb.index(self.nb.select()) == 0:
            lst = self.lst_date
        else:
            lst = self.lst_bkmrk    
        
        if lst.size() > 0:
            selection = lst.curselection()[0]
            if selection > 0:
                lst.selection_clear(0,'end')
                lst.selection_set(selection - 1, selection - 1)
                lst.see(lst.curselection())
                lst.event_generate('<<ListboxSelect>>')
        
    def forward(self):
        if self.nb.index(self.nb.select()) == 0:
            lst = self.lst_date
        else:
            lst = self.lst_bkmrk    
        
        if lst.size() > 0:
            selection = lst.curselection()[0]
            if selection < lst.size() -1 :
                lst.selection_clear(0,'end')
                lst.selection_set(selection + 1, selection + 1)
                lst.see(lst.curselection())
                lst.event_generate('<<ListboxSelect>>')

    def sync(self):
        try:
            msg = gc.update_comics(gc.con)
            messagebox.showinfo('Sync',msg)
        except Exception as e:
            messagebox.showerror('Error',e)

    def save_comic(self):
        try:
            # imgtype = imghdr.what('',self.comic)      # not using since imghdr is being deprecated
            
            dr = str(Path(__file__).parent.resolve(True))
            dr = dr + '/dilbert_strips'
            Path(dr).mkdir(exist_ok=True)
            
            filename = dr + f'/{self.comic_date}.{self.imgtype}'
            # print(filename)
            with open(filename,'wb') as f:
                f.write(self.comic)
            messagebox.showinfo('Save',f'Comic image saved at:\n\n{filename}')
        except Exception as e:
            messagebox.showerror('Error',e)

    def fill_bookmarks(self):
        self.bookmarks_arr = gc.get_bookmarks()
        self.bookmarks.set(self.bookmarks_arr)

    def toggle_bookmark(self):
        self.bkmrk.set(not self.bkmrk.get() )
        self.set_bookmark()

    def set_bookmark(self):
        if self.bkmrk.get():
            with gc.con:
                gc.cur.execute('insert into bookmarks values(?);',(self.comic_date,))
            print(f'Bookmark set for {self.comic_date}')
        else:
            with gc.con:
                gc.cur.execute('delete from bookmarks where date = ?;',(self.comic_date,))
            print(f'Bookmark removed for {self.comic_date}')
        self.fill_bookmarks()

    def get_random(self):
        ry = random.choice(self.years_arr)
        rm = random.choice(self.months_arr)
        self.years.set(ry)
        self.months.set(rm)
        
        self.dates_ar = gc.get_dates(self.years.get(),self.months.get())
        self.dates.set(self.dates_ar)
        self.lst_date.selection_clear(0,'end')
        
        rd = random.randint(0,len(self.dates_ar)-1)

        self.lst_date.selection_set(rd,rd)
        self.lst_date.see(self.lst_date.curselection())
        self.lst_date.event_generate('<<ListboxSelect>>')


def main():
    Dilbert()


if __name__ == '__main__':
    main()
