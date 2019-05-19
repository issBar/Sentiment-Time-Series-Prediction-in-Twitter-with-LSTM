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
from PIL import Image, ImageTk
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

frame_size="700x400"
backround_color='#32afea'
text_color='#575661'
button_backroud_color='#8db3c3'


x_size=500
y_size=500

def get_duration(*args):
    return time_options[variable.get()]



class app(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry(frame_size)
        self.configure(bg=backround_color)
        self._frame = None
        self.start_frame(StartPage)
        self.resizable(False,False)
        
    def start_frame(self,frame_class):
         """Destroys current frame and replaces it with a new one."""
         new_frame = frame_class(self)
         if self._frame is not None:
             self._frame.destroy()
         self._frame = new_frame
         self._frame.pack()
        
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
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=backround_color)
        #fonts
        #small_font =Font(family="Courier",size=6,weight="bold")
        self.large_font= Font(family="Courier",size=24,weight="bold")
        self.meduim_font=Font(family="Courier",size=12,weight="bold")
        
    
        #top frame
        topframe=Frame(self,bg=backround_color)
        topframe.pack()
        login_button=Button(topframe,text="Login",command=lambda : master.start_frame(twitter_login),bg=button_backroud_color)
        login_button.pack(side=RIGHT)
        #top_label
        top_label=Label(topframe,text="Welcome",fg="white",bg=backround_color,font=large_font)       
        top_label.pack(fill=tk.X,pady=10,side=TOP)
        #label
        label_h=Label(topframe,text="Insert requested Hashtag for Prediction : #",fg=text_color,font=self.meduim_font,bg=backround_color)
        label_h.pack(pady=10,side=LEFT)
        #TextBox
        textbox_h=Entry(topframe)
        textbox_h.pack(padx=5,side=RIGHT)
    
        #middel frame
        midframe=Frame(self,bg=backround_color)
        midframe.pack()
        
        #label
        label_ts=Label(midframe,text="Set Duration of a Time-Series : ",fg=text_color,font=self.meduim_font,bg=backround_color)
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
        
        #run button
        run_button=Button(lowframe,fg=text_color,text="Run",font=self.meduim_font,command=lambda: self.check_input(master,textbox_h,duration),bg=button_backroud_color)
        run_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        run_button.pack(fill=tk.X,padx=5,side=TOP)
   
       #mid_label
        label_uploadfile=Label(lowframe,text="OR",fg="white",bg=backround_color,font=self.meduim_font)       
        label_uploadfile.pack(pady=10,side=TOP)
    
       #uploadFile
        up_search_button=Button(lowframe,fg=text_color,text="Choose file",font=self.meduim_font,bg=button_backroud_color)
        up_search_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        up_search_button.pack(fill=tk.X,pady=10,side=TOP)
        
        
    def check_input(self,master,textbox_h,duration):
        if re.match("^[A-Za-z0-9_-]*$", textbox_h.get()):
            master.switch_frame(StatusPage,textbox_h,duration)
        else:
            messagebox.showinfo("Information","can only accept a-z ,A-Z,0-9")        
    


class StatusPage(tk.Frame):
    
    def __init__(self,master,textbox_h,duration):
        tk.Frame.__init__(self,master)
        self.configure(bg=backround_color)
        
        #small_font =Font(family="Courier",size=6,weight="bold")
        #large_font =Font(family="Courier",size=24,weight="bold")
        self.meduim_font=Font(family="Courier",size=12,weight="bold")
        
        
        #top frame
        self.topFrame=Frame(self,bg=backround_color)
        self.topFrame.pack(fill="both", expand=True, padx=100, pady=80)
        
        #back button
        self.back_button=Button(self.topFrame,fg=text_color,text="Back",command=lambda:master.switch_frame(StartPage,None,None),font=self.meduim_font,bg=button_backroud_color)
        self.back_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
                              
        self.back_button.pack(pady=10,side=BOTTOM)
        #label status
        self.label_status=Label(self.topFrame,text="Status",bg=backround_color,font=self.meduim_font)
        self.label_status.pack(pady=10,side=TOP)
        
        #prograss bar
        self.progressBar = Progressbar(self.topFrame,orient="horizontal",style="red.Horizontal.TProgressbar",length=350,  mode="determinate")
        self.progressBar.pack(side=LEFT)
        self.input_=textbox_h.get()
        
        #time label
        self.time_lable=Label(self.topFrame,text="time:"+,bg=backround_color,font=self.meduim_font)
        self.time_lable.pack(side=RIGHT)
        
        
        #start theread 
        self.start_submit_thread(self.input_,duration,progressBar,True,master)
        
    def start_submit_thread(self,TEXT,duration,progressBar,flag,master):
        global submit_thread
        global lock
        lock=threading.Lock()
        submit_thread = threading.Thread(target=lambda : self.run(TEXT,duration,progressBar,flag,master))
        submit_thread.daemon = True
        submit_thread.start()
        
   
        
    def run(self,text,duration,progressBar,flag,master):
        duration=int(duration)
        try:
            lock.acquire()
            tweets_len=0
            if(flag==True):
                #connection to twitter and geting tweets
                hours=duration*24
                
                #progressbar
                p_size=(hours*10)+100
                progressBar['maximum']=p_size
                self.time_lable.text='estimated time:'+
                #for testing
                tweets_len+=TweetCon.runTweetCon(text,0)
                print("fatching size=",tweets_len)
                progressBar['value']=p_size-100
                
                '''
                #loop for taking tweet by hours
                for d in hours:
                    TweetCon.runTweetCon(text,0)
                    progressBar['value']+=10
                    time.sleep(3600)
                '''
                #run preprocess
                preprocess.runPreprocess(2,text)
                progressBar['value']+=25
                
                NLP.run_natural_language_processing(text,True)
                progressBar['value']+=25
                
                timeSeries.run_time_series(text,True)
                progressBar['value']+=25
                
                dt_dic,time_,pred=LSTM_ver2.run_LSTM("Trump")
                progressBar['value']+=25
                
                master.switch_frame_plt(PlotPage,text,duration,master,dt_dic,time_,pred)
                #result_page(text,date_time_dic)
            #else:   
                #date_time_dic=timeSeries.run_time_series('',False)
                #result_page('',date_time_dic)
                
            lock.release()
                  
        except KeyboardInterrupt as err:
            print(err)
            
            

class PlotPage(tk.Frame):
   
    def __init__(self,text,duration,master,dt_dic,time_,pred):
        tk.Frame.__init__(self, master)
        self.text=text
        #top frame
        self.meduim_font=Font(family="Courier",size=12,weight="bold")
        self.topFrame=Frame(self,bg=backround_color)
        self.topFrame.pack()
        
        
        self.back_button=Button(self.topFrame,fg=text_color,text="Back",command=lambda:master.switch_frame(StartPage,text,None),font=self.meduim_font,bg=button_backroud_color)
        self.back_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        self.back_button.pack(side=LEFT)
              
        #middle frame
        self.middleFrame=Frame(self,bg=backround_color)
        self.middleFrame.pack()

        
        self.run_canvas(dt_dic,time_,pred,text, self.topFrame)
        
    def run_canvas(self,dt_dic,time_,pred,text,topFrame):
        
         #array of buttons
         buttons=[]
         
         #array of label
         plots_labels = Label(self.topFrame)
         plots_labels.images=[]
         count_plots=[]
         #Plotting graphs by Date and Hours 
         for i in range(len(dt_dic)):
             count_plots.append(i)
         
         print("count_plots= ",count_plots)
         count=0
         for key,value in dt_dic.items():
             self.text='Trump'
             self.image_path='./csvData/'+self.text+'/plots/'+self.text+'_plot_'+key+'.png'
             plots_labels.images.append(PhotoImage(file=self.image_path))
             buttons.append(Button( self.middleFrame,fg=text_color,text=key,command= lambda  x=count_plots[count] :self.open_canvas(plots_labels,x)).pack(side=LEFT))
             count+=1
         image_path_pred='./csvData/'+self.text+'/plots/'+self.text+'_plot_prediction.png'
         plots_labels.images.append(PhotoImage(file=image_path_pred))
         buttons.append(Button(self.middleFrame,fg=text_color,text=key,command= lambda  x=count :self.open_canvas(plots_labels,x)).pack(side=LEFT))

         
            

             
    def open_canvas(self,plots_labels,count):
        self.text='Trump'
        
        plots_labels.images
        
        plots_labels.config(image=plots_labels.images[count])
        plots_labels.pack()
          
        
    
class twitter_login(tk.Frame):
   
    def __init__(self,master):
        tk.Frame.__init__(self,master)
       # self.configure(bg=backround_color)
        print("-----twitter login-----")
        #small_font = font.Font(family="Montserrat",size="8",weight="bold")
        #large_font= font.Font(family="Montserrat",size="24",weight="bold")
        #meduim_font=Font(family="Montserrat",size=16,weight="bold")
        #font.families()
        twitt_login=Frame(self,bg=backround_color)
        

        fields=   'Consumer Key','Consumer Secret','Access Token','Access Token Secret'
        inputs = []
        for field in fields:
            row = Frame(twitt_login)
            labels = Label(row, width=15, text=field, anchor='w')
            entries = Entry(row, width=45)
            row.pack(side=TOP, fill=X, padx=5, pady=15)
            labels.pack(side=LEFT)
            entries.pack(side=RIGHT, expand=YES, fill=X)
            inputs.append((field, entries))


        twitt_login.pack(anchor='center')

        #messagebox.showinfo("Information", "1.Login to your Twitter account on developer.twitter.com\n2.Navigate to the Twitter app dashboard and open the Twitter app for which you would like to generate access tokens.\n3.Navigate to the Keys and Tokens page.\n4.Select Create under the Access token & access token secret section.")
        info = Label(twitt_login,text="Please follow steps: \n1.Login to your Twitter account on developer.twitter.com\n2.Navigate to the Twitter app dashboard and open the Twitter app for which you would like to generate access tokens.\n3.Navigate to the Keys and Tokens page.\n4.Select Create under the Access token & access token secret section.")
        info.pack(side=BOTTOM,fill=BOTH)
    
        
if __name__ == "__main__":
    app = app()
    app.mainloop()
    