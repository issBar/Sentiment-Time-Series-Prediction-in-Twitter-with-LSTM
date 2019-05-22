#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 01:07:19 2019

@author: yaron
"""


frame_size="820x420"
backround_color='white'
text_color='#68696B'
login_toplabel_color='#3898DB'
button_backroud_color='#E7EDF1'


import TweetCon 
import NLP
import preprocess 
import timeSeries
import LSTM_ver2
import utility
from importlib import reload  # Python 3.4+ only.
import threading
from PIL import Image, ImageTk
import time
import re

NLP=reload(NLP)
TweetCon=reload(TweetCon)
preprocess=reload(preprocess)
timeSeries=reload(timeSeries)
import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk
from tkinter import messagebox


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.geometry(frame_size)
        #self.configure(bg=backround_color)
        #self.resizable(False,False)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        barFrame=tk.Frame(self)
        toplabel=tk.Label(barFrame,bg=login_toplabel_color)
        toplabel.pack(side="top",fill="both")
        barFrame.pack(side="top",fill="both")
        
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (StartPage, PageOne,TwitterLogin):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nswe")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]

        frame.tkraise()
        
    def show_status_frame(self,parent,status_class,text,duration):
        st_page=status_class(parent,self,text,duration)
        st_page.grid(row=0, column=0, sticky="nsew")
        st_page.tkraise()






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
        login_button=tk.Button(top_frame,text="Login",state=tk.ACTIVE,fg=login_toplabel_color,command=lambda : controller.show_frame("TwitterLogin"),bg=button_backroud_color)
                
        
        #login_button['state'] = tk.DISABLED

        login_button.pack(side="right",padx=10)
        #top_label
        top_label=tk.Label(top_frame,text="Twitter prediction",fg=text_color,font=controller.title_font)       
        top_label.pack(side="top",anchor="center")
        
        #middleFrame
        middleFrame_frame=tk.Frame(self)
        middleFrame_frame.pack_propagate(1)
        middleFrame_frame.pack(fill="both",side="top",pady=20,padx=25)
        #label
        label_h=tk.Label(middleFrame_frame,text="Insert Hashtag for Prediction :",fg=text_color)
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
        separator.pack(side="top",padx=25,fill='both')

        #Bottom Frame
        bottomFrame=tk.Frame(self)
        bottomFrame.pack(side="top",fill="both",padx=25,pady=25)

        #label
        label_ts=tk.Label(bottomFrame,text="Set Duration of a Time-Series : ",fg=text_color)
        label_ts.pack(side="left")
        #option bar
        time_options={"1 Day":1,"2 Days":2,"3 Days":3,"4 Days":4,"5 Days":5,"6 Days":6,"7 Days":7}
        variable=tk.StringVar(bottomFrame)
        variable.set("1 Day")
        option_menu_time=tk.OptionMenu(bottomFrame,variable,*time_options.keys())
        option_menu_time.config(bg=button_backroud_color,activebackground=button_backroud_color)
        option_menu_time.pack(side="left")
        variable.trace("w",self.get_duration)

        duration=(variable.get()).split('Day')[0]
        
        runFrame=tk.Frame(self)
        runFrame.pack(side="top",fill="both",padx=25,pady=25)
        #run button
        run_button=tk.Button(runFrame,fg=text_color,text="Run",command=lambda: self.check_input(parent,self.textbox_h,duration),bg=button_backroud_color)
        run_button.configure(width = 10, activebackground = "#33B5E5", relief = tk.FLAT)
        run_button.pack(anchor="center")

        
        
    def check_input(self,parent,textbox_h,duration):
        
        if re.match("^[A-Za-z0-9_-]*$", textbox_h.get()):
            
            self.controller.show_status_frame(parent,StatusPage,textbox_h,duration)
            
        else:
            messagebox.showinfo("Information","can only accept a-z ,A-Z,0-9")        
       
    
    def get_duration(self,*args):
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


class TwitterLogin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="return",command=lambda: controller.show_frame("StartPage"))
        button.pack(anchor="w",padx=7,pady=3)
        login_label=tk.Label(self,text="Get Twitter Developer Access :",font=controller.title_font)
        login_label.pack(anchor="ne",fill="x",pady=5)
        self.cons_key=""
        
        
        twitt_login=tk.Frame(self)
        twitt_login.place(x=0, y=0, width=400, height=600)
        
        fields='Consumer Key','Consumer Secret','Access Token','Access Token Secret'
        inputs = {}
        entries=[]
        for field in fields:
            row = tk.Frame(twitt_login)
            labels = tk.Label(row, width=15, text=field, anchor='w',fg=text_color)
            entry = tk.Entry(row, width=45,bg=button_backroud_color)
            entries.append(entry)
            row.pack(side="top",fill='both', padx=5, pady=15)
            labels.pack(side="left")
            entry.pack(side="right",padx=3, expand=1, fill='both')
            inputs[field]=entry.get()

                      
        self.verify_acc=tk.Button(twitt_login,text="Verify",bg=button_backroud_color,fg=login_toplabel_color,command=lambda: self.verify_inputs(entries))
        self.verify_acc.pack(side='right',padx=10,pady=10) 
     
        twitt_login.pack(side="left")

        
        separator = ttk.Separator(self, orient='vertical')
        separator.pack(side="left",fill='both',padx=15,pady=25)
        
        info_frame=tk.Frame(self)
        
        label1=tk.Label(info_frame,text="Please follow steps:\n")
        label1.pack(anchor="w")
        label2=tk.Label(info_frame,text="1. Login to your Twitter account on : http://www.developer.twitter.com")
        label2.pack(anchor="w")
        label3=tk.Label(info_frame,text="2. Navigate to the Twitter app dashboard and open the Twitter\napp for which you would like to generate access tokens.")
        label3.pack(anchor="w")
        label4=tk.Label(info_frame,text="3. Navigate to the Keys and Tokens page.")
        label4.pack(anchor="w")
        label5=tk.Label(info_frame,text="4. Select Create under the Access token & access token secret section.")
        label5.pack(anchor="w")

        #info.bind("<Button-1>", self.callback)
        info_frame.pack(side=tk.LEFT,anchor="center")
        
              
                
    def verify_inputs(self,entries):
        
        #inputs received from entries 
        #consumer_key=entries[0].get()
        #consumer_secret=entries[1].get()
        #access_token=entries[2].get()
        #access_token_secret=entries[3].get()
        

        consumer_key = 'i5UW3ELVfZMBo7v9QfJ5bBK4q'
        consumer_secret = 'PzNZLrr8zdvEi3MkHv43mkA6GmgwP8g6J12eDAsfU1HiYpGtZ7'
        access_token = '469641234-wAc1uMHBENJwI5S0SUFdED63dMlWwTTTdOVHIrOL'
        access_token_secret = '3DSGRzcuFEnRIPzIQaRn17e2xXBARKh1fTlis1H1tGHz5'
        
        import time
        import tweepy
        # if consumer_key==None
        try:
            if len(consumer_key)!=0 and len(consumer_secret)!=0 and len(access_token)!=0 and len(access_token_secret)!=0:
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth, wait_on_rate_limit=True)
               
                #show user name
                user = api.me()
                print("success : ",user.name)
                time.sleep(1)
                tk.messagebox.showinfo(message="Success login to : "+user.name)
                self.controller.show_frame("StartPage")

            else:
                tk.messagebox.showinfo(message="Check your inputs")

        except: 
             print("Error: Authentication Failed") 


        
    def on_enter(self, event):
        self.information_label.configure(text=self.event)

    def on_leave(self, enter):
        self.information_label.configure(text=self.event)
      
        
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

        
class StatusPage(tk.Frame):
    
    def __init__(self,parent,controller,textbox_h,duration):
        tk.Frame.__init__(self,parent)
        self.controller = controller

       
        #top frame
        self.topFrame=tk.Frame(self)
        self.topFrame.pack(fill='x',side=tk.TOP,anchor="n")
        #back button
        self.back_button=tk.Button(self.topFrame,fg=text_color,text="Back",command=lambda:self.controller.show_frame("StartPage"),bg=button_backroud_color)
        self.back_button.configure(width = 10, activebackground = "#33B5E5", relief = tk.FLAT)
        self.back_button.pack(padx=10,pady=10,side=tk.LEFT) 
        
        #status frame
        self.statusFrame=tk.Frame(self)
        self.statusFrame.pack(fill='x',side=tk.TOP,anchor="n")
     
        #label status
        self.label_status=tk.Label(self.statusFrame,text="Processing...",font=controller.title_font)
        self.label_status.pack(side=tk.TOP,pady=10,anchor="center")
        
        #center Frame
        self.centerFrame=tk.Frame(self)
        self.centerFrame.pack(pady=10,side=tk.TOP)
            
        
        #time label
        self.var = tk.StringVar()
        self.var.set('Time left:')
        self.time_label=tk.Label(self.centerFrame,textvariable=self.var)
        self.time_label.pack(side=tk.BOTTOM)
                      
    
        #progress bar
        self.progressBar =ttk.Progressbar(self.centerFrame,orient="horizontal",style="red.Horizontal.TProgressbar",length=350,  mode="determinate")
        self.progressBar.pack(side=tk.RIGHT,anchor='center')
        self.input_=textbox_h.get()
 
   
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(side=tk.TOP,fill='both',padx=15,pady=5)
        
        #details Frame
        self.detailsFrame=tk.Frame(self)

        texts_for_labels='Fetching Tweets','Preprocess Tweets','Sentiment Analysis','LSTM Prediction'
        self.checkboxes={}
        self.checkbox_fetchs_tweets={}
        for text_l in texts_for_labels:
            row = tk.Frame(self.detailsFrame)
            label=tk.Label(row,text=text_l,fg=text_color)
            self.checkboxes[text_l]=tk.Variable()
            checkbox_fetch_tweets=tk.Checkbutton(row,state=tk.DISABLED,variable=self.checkboxes[text_l])
            row.pack(side="top",fill='both', padx=15, pady=10)
            label.pack(side=tk.LEFT)
            checkbox_fetch_tweets.pack(side=tk.RIGHT)
            checkbox_fetch_tweets.deselect()
            self.checkbox_fetchs_tweets[text_l]=checkbox_fetch_tweets

        self.detailsFrame.pack(side=tk.LEFT)

        
        
        #start thread 
        self.start_submit_thread(self.input_,duration,True,controller)
        
        
    def start_submit_thread(self,TEXT,duration,flag,master):
        global submit_thread
        global lock
        lock=threading.Lock()
        submit_thread = threading.Thread(target=lambda : self.run(TEXT,duration,flag,master))
        submit_thread.daemon = True
        submit_thread.start()
        
   
    def run(self,text,duration,flag,master):
        duration=int(duration)
        try:
            lock.acquire()
        
            if(flag==True):
                #connection to twitter and getting tweets
                hours=duration*24
                print("Processing hours : ",hours)
                #progressbar
                p_size=(hours*10)+60
                self.progressBar['maximum']=p_size
                self.var.set('Time left: Processing...')

                print("tktktktk : " ,hours)
                #loop for taking tweet by hours
                for i in range(hours):
                    print("Fetch number : ",(i+1),'/',hours)
                    TweetCon.runTweetCon(text,0)
                    self.progressBar['value']+=10     
                    self.var.set('Time left: {} Hours'.format(hours+3-i))

                    time.sleep(1)
                            
                self.checkbox_fetchs_tweets['Fetching Tweets'].select()


                #run preprocess
                preprocess.runPreprocess(2,text)
                self.progressBar['value']+=20
                self.checkbox_fetchs_tweets['Preprocess Tweets'].select()

                NLP.run_natural_language_processing(text,True)
                self.progressBar['value']+=20
                self.checkbox_fetchs_tweets['Sentiment Analysis'].select()

                timeSeries.run_time_series(text,True)
                dt_dic,time_,pred=LSTM_ver2.main_pred("Trump")
                self.progressBar['value']+=20
                self.checkbox_fetchs_tweets['LSTM Prediction'].select()
                
                #master.switch_frame_plt(PlotPage,text,duration,master,dt_dic,time_,pred)
                #result_page(text,date_time_dic)
            #else:   
                #date_time_dic=timeSeries.run_time_series('',False)
                #result_page('',date_time_dic)
                
            lock.release()
                  
        except KeyboardInterrupt as err:
            print(err)
            
                    

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()