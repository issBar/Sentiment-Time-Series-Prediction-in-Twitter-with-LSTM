#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 15:18:23 2019

@author: yaron
"""

import TweetCon 
import NLP
import preprocess 
import timeSeries
import LSTM_ver2
import utility
from importlib import reload  # Python 3.4+ only.
import threading
import tkinter as tk
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.font import Font
from PIL import Image, ImageOps
import time
import re
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
NLP=reload(NLP)
TweetCon=reload(TweetCon)
preprocess=reload(preprocess)
timeSeries=reload(timeSeries)

frame_size="650x350"
backround_color='#32afea'
text_color='#575661'
button_backroud_color='#8db3c3'

x_size=500
y_size=500



def check_input(master,textbox_h,duration):
    if re.match("^[A-Za-z0-9_-]*$", textbox_h.get()):
        master.switch_frame(StatusPage,textbox_h,duration)
    else:
        messagebox.showinfo("Information","can only accept a-z ,A-Z,0-9")        
    
def start_submit_thread(TEXT,duration,progressBar,flag,master):
 
    global submit_thread
    global lock
    lock=threading.Lock()
    submit_thread = threading.Thread(target=lambda : run(TEXT,duration,progressBar,flag,master))
    submit_thread.daemon = True
    submit_thread.start()



def run(text,duration,progressBar,flag,master):
    duration=int(duration)
    try:
        lock.acquire()
        
        if(flag==True):
            TweetCon.runTweetCon(text,0)
            progressBar['value']=60
            
            preprocess.runPreprocess(2,text)
            progressBar['value']+=10
            
            NLP.run_natural_language_processing(text,True)
            progressBar['value']+=15
            
            timeSeries.run_time_series(text,True)
            progressBar['value']+=5
            
            dt_dic,time_,pred=LSTM_ver2.run_LSTM("Trump")
            progressBar['value']+=10
            
            master.switch_frame_plt(PlotPage,text,duration,master,dt_dic,time_,pred)
            #result_page(text,date_time_dic)
        else:   
            date_time_dic=timeSeries.run_time_series('',False)
            #result_page('',date_time_dic)
            
        lock.release()
              
    except KeyboardInterrupt as err:
        print(err)
        

def get_duration(*args):
    return time_options[variable.get()]


def qeustionButton(root,sides):
    file='./qes-icon.png'
    photo=PhotoImage(file=file)
    qbutton=Button(root)
    qbutton.config(image=photo,width="20",height="20")
    qbutton.pack(fill=tk.X,padx=5,pady=10,side=sides)
    

class app(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry(frame_size)
        self.configure(bg=backround_color)
        self._frame = None
        self.switch_frame(StartPage,None,None)

    def switch_frame(self, frame_class,text,duration):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self,text,duration)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        
    def switch_frame_plt(self, frame_class,text,duration,master,dt_dic,time_,pred):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(text,duration,master,dt_dic,time_,pred)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    
    def __init__(self, master,text,duration):
        tk.Frame.__init__(self, master)
        self.configure(bg=backround_color)
        small_font =Font(family="Courier",size=6,weight="bold")
        large_font= Font(family="Courier",size=24,weight="bold")
        meduim_font=Font(family="Courier",size=12,weight="bold")
        
    
        #top frame
        topframe=Frame(self,bg=backround_color)
        topframe.pack()
        #top_label
        top_label=Label(topframe,text="Welcome",fg="white",bg=backround_color,font=large_font)       
        top_label.pack(fill=tk.X,pady=10,side=TOP)
        #label
        label_h=Label(topframe,text="Insert requested Hashtag for Prediction : #",fg=text_color,font=meduim_font,bg=backround_color)
        label_h.pack(pady=10,side=LEFT)
        #TextBox
        textbox_h=Entry(topframe)
        textbox_h.pack(padx=5,side=RIGHT)
    
        #middel frame
        midframe=Frame(self,bg=backround_color)
        midframe.pack()
        
        #label
        label_ts=Label(midframe,text="Set Duration of a Time-Series : ",fg=text_color,font=meduim_font,bg=backround_color)
        label_ts.pack(pady=10,side=LEFT)
        #option bar
        time_options={"1 Day":1,"2 Days":2,"3 Days":3,"4 Days":4,"5 Days":5,"6 Days":6,"7 Days":7}
        variable=StringVar(midframe)
        variable.set("1 Day")
        option_menu_time=OptionMenu(midframe,variable,*time_options.keys())
        option_menu_time.config(bg=button_backroud_color,activebackground=button_backroud_color)
        option_menu_time.pack(pady=10,side=RIGHT)
        variable.trace("w",get_duration)

        #low frame
        lowframe=Frame(self,bg=backround_color)
        lowframe.pack()
    
        duration=(variable.get()).split('Day')[0]
        print(duration)
        #searchButton
        new_search_button=Button(lowframe,fg=text_color,text="Run",font=meduim_font,command=lambda: check_input(master,textbox_h,duration),bg=button_backroud_color)
        new_search_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        new_search_button.pack(fill=tk.X,padx=5,side=TOP)
   
       #mid_label
        label_uploadfile=Label(lowframe,text="OR",fg="white",bg=backround_color,font=meduim_font)       
        label_uploadfile.pack(pady=10,side=TOP)
    
       #uploadFile
        up_search_button=Button(lowframe,fg=text_color,text="Choose file",font=meduim_font,bg=button_backroud_color)
        up_search_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        up_search_button.pack(fill=tk.X,pady=10,side=TOP)
        


class StatusPage(tk.Frame):
    def __init__(self,master,textbox_h,duration):
        tk.Frame.__init__(self,master)
        self.configure(bg=backround_color)
        small_font = font.Font(family="Montserrat",size="8",weight="bold")
        large_font= font.Font(family="Montserrat",size="24",weight="bold")
        meduim_font=Font(family="Montserrat",size=16,weight="bold")
        font.families()
        print('text:',textbox_h.get())
        print("DURATION : ",duration)
        topFrame=Frame(self,bg=backround_color)
        topFrame.pack(fill="both", expand=True, padx=100, pady=80)
        
        back_button=Button(topFrame,fg=text_color,text="Back",command=lambda:master.switch_frame(StartPage,None,None),font=meduim_font,bg=button_backroud_color)
        back_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        back_button.pack(pady=10,side=BOTTOM)
        
        label_status=Label(topFrame,text="Status",bg=backround_color,font=meduim_font)
        label_status.pack(pady=10,side=TOP)
    
        progressBar = Progressbar(topFrame,orient="horizontal",style="red.Horizontal.TProgressbar",length=350,  mode="determinate")
        progressBar.pack(side=LEFT)
        input_=textbox_h.get()
        start_submit_thread(input_,duration,progressBar,True,master)
        
        
     
            

class PlotPage(tk.Frame):
   
    def __init__(self,text,duration,master,dt_dic,time_,pred):
        tk.Frame.__init__(self, master)
        self.topFrame=Frame(self,bg=backround_color)
        self.topFrame.pack()
        
        self.mideelFrame=Frame(self,bg=backround_color)
        self.mideelFrame.pack()
        
        self.run_canvas(dt_dic,time_,pred,text, self.topFrame)
        
    def run_canvas(self,dt_dic,time_,pred,text,topFrame):
         f=plt.figure()
         x_axis=[]
         y_axis=[]
         buttons=[]
         #Plotting graphs by Date and Hours 
         for key,value in dt_dic.items():
             for x in value:
                 x_axis.append(x[0])
                 y_axis.append(x[1])     
         
             f.suptitle('Next Hour Prediction',fontsize=12)
             plt.figure(figsize=(10 , 6))
             plt.ylim([-1,1])
             plt.title("#"+text+" prediction graph for date : "+key)
             plt.plot(x_axis,y_axis,label=key,marker='o',markersize=8)
             plt.gcf().autofmt_xdate(bottom=0.3, rotation=50, ha='right', which=None)
             plt.xlabel('Time-Series',fontsize=16)
             plt.ylabel('Predict',fontsize=16)
             x_axis=[]
             y_axis=[]
             buttons.append(tk.Button(topFrame,fg=text_color,text=key,command= lambda: self.open_canvas(plt)).pack(side=LEFT))
         split_date=time_.split(' ')
         plt.plot(split_date[1],pred,marker='s')
         buttons.append(tk.Button(topFrame,fg=text_color,text=key,command= lambda: self.open_canvas(plt)).pack(side=LEFT))
         
    def open_canvas(self,plt):
        #Plotting predicted value
         
        
         canvas = FigureCanvasTkAgg(plt.figure(), self.mideelFrame)
         canvas.show()
         canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
         toolbar = NavigationToolbar2TkAgg(canvas,  self.mideelFrame)
         toolbar.update()
         canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)    
    
        
        
if __name__ == "__main__":
    app = app()
    app.mainloop()
    