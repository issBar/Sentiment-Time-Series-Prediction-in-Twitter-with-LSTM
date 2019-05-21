#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 01:07:19 2019

@author: yaron
"""


frame_size="600x300"
backround_color='#FFFFFF'
text_color='#9F9F9F'
login_toplabel_color='#3898DB'
button_backroud_color='#E7EDF1'


import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2




class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=24, weight="bold")
        self.geometry(frame_size)
        self.configure(bg=backround_color)
        
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        barFrame=tk.Frame(self)
        toplabel=tk.Label(barFrame,bg=login_toplabel_color)
        toplabel.pack(side="top",fill="both")
        barFrame.pack(side="top",fill="both")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo,TwitterLogin):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        #topFrame
        top_frame=tk.Frame(self)
        top_frame.pack_propagate(1)
        top_frame.place(x=0,y=0)
        top_frame.pack(fill="both",padx=5,pady=5)
        #login button
        login_button=tk.Button(top_frame,text="Login",fg=login_toplabel_color,command=lambda : controller.show_frame("TwitterLogin"),bg=button_backroud_color)
        login_button.pack(side="right",padx=10)
        #top_label
        top_label=tk.Label(top_frame,text="Twitter prediction",fg=text_color,bg=backround_color,font=controller.title_font)       
        top_label.pack(side="top",anchor="center")
        
        #middleFrame
        middleFrame_frame=tk.Frame(self)
        middleFrame_frame.pack_propagate(1)
        middleFrame_frame.pack(fill="both",side="top",pady=20,padx=25)
        #label
        label_h=tk.Label(middleFrame_frame,text="Insert Hashtag for Prediction :",fg=text_color,bg=backround_color)
        label_h.pack(side="left",anchor="w")

        #TextBox
        self.textbox_h=tk.Entry(middleFrame_frame,bg=button_backroud_color)
        self.textbox_h.insert(0, 'Insert Hashtag..')
        self.textbox_h.bind('<FocusIn>', self.on_entry_click)
        self.textbox_h.bind('<FocusOut>', self.on_focusout)
        self.textbox_h.config(fg = 'grey')
        self.textbox_h.pack(side="left",anchor="e")
        
        #separator
        self.sep_style=ttk.Style()
        self.sep_style.configure('s.TSeparator',foreground='green')
        separator = ttk.Separator(self, orient='horizontal',style='s.TSeparator')
        separator.pack(side="top",padx=25,fill=X)

        #Bottom Frame
        bottomFrame=tk.Frame(self)
        bottomFrame.pack(side="top",fill="both",padx=25,pady=25)

        #label
        label_ts=Label(bottomFrame,text="Set Duration of a Time-Series : ",fg=text_color,bg=backround_color)
        label_ts.pack(side="left")
        #option bar
        time_options={"1 Day":1,"2 Days":2,"3 Days":3,"4 Days":4,"5 Days":5,"6 Days":6,"7 Days":7}
        variable=StringVar(bottomFrame)
        variable.set("1 Day")
        option_menu_time=OptionMenu(bottomFrame,variable,*time_options.keys())
        option_menu_time.config(bg=button_backroud_color,activebackground=button_backroud_color)
        option_menu_time.pack(side="left")
        variable.trace("w",get_duration)

        duration=(variable.get()).split('Day')[0]
        
        runFrame=tk.Frame(self)
        runFrame.pack(side="top",fill="both",padx=25,pady=25)
        #run button
        run_button=tk.Button(runFrame,fg=text_color,text="Run",command=lambda: self.check_input(controller,self.textbox_h,duration),bg=button_backroud_color)
        run_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        run_button.pack(anchor="center")

        
        
    def check_input(self,controller,textbox_h,duration):
        if re.match("^[A-Za-z0-9_-]*$", textbox_h.get()):
            controller.show_frame(PageOne,self.textbox_h,duration)
        else:
            messagebox.showinfo("Information","can only accept a-z ,A-Z,0-9")        
    
    
    
    def get_duration(*args):
        return time_options[variable.get()]


    def on_entry_click(self,event):
        """function that gets called whenever entry is clicked"""
        if self.textbox_h.get() == 'Insert Hashtag..':
            self.textbox_h.delete(0, "end") # delete all the text in the entry
            self.textbox_h.insert(0, '') #Insert blank for user input
            self.textbox_h.config(fg = text_color)
            
    def on_focusout(self,event):
        if self.textbox_h.get() == '':
            self.textbox_h.insert(0, 'Insert Hashtag..')
            self.textbox_h.config(fg=text_color)




class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",command=lambda: controller.show_frame("StartPage"))
        button.pack()


class TwitterLogin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()