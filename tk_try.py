#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 01:07:19 2019

@author: yaron
"""


frame_size="700x600"
backround_color='white'
text_color='#3d3d3d'
login_toplabel_color='#3898DB'
button_background_color='#E7EDF7' #real #E7EDF1

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import TweetCon 
import NLP
import preprocess 
import timeSeries
import LSTM_ver2
import utility as util
from importlib import reload  # Python 3.4+ only.
import threading
from PIL import Image, ImageTk
import time
import re
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tweepy
import DataBase


NLP=reload(NLP)
TweetCon=reload(TweetCon)
preprocess=reload(preprocess)
timeSeries=reload(timeSeries)
DataBase=reload(DataBase)
import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk
from tkinter import messagebox
#from tkthread import tk, TkThread



class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #'HELP' Menu Bar
        self.menubar = tk.Menu(self)
        self.fileMenu = tk.Menu(self.menubar)
        self.fileMenu.add_command(label="READ ME", command=self.load_README)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.destroy)
        self.config(menu=self.menubar)
        self.menubar.add_cascade(label="Help", menu=self.fileMenu)

        # FONTS
        self.title_font = tkfont.Font(family='Verdana', size=20, weight="bold")
        self.semi_font=tkfont.Font(family="comic sans ms", size=8)
        self.text_font = tkfont.Font(family='Verdana', size=12, weight="bold")

        self.geometry(frame_size)

        #self.resizable(False,False)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        barFrame=tk.Frame(self)
        toplabel=tk.Label(barFrame,bg=button_background_color)
        toplabel.pack(side="top",fill="both")
        barFrame.pack(side="top",fill="both")
        
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage,TwitterLogin):
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
        
    def show_status_frame(self,parent,status_class,text,duration,scale):
        st_page=status_class(parent,self,text,duration,scale)
        st_page.grid(row=0, column=0, sticky="nsew")
        st_page.tkraise()
        
        
    def show_plots_frame(self,parent,PlotPage_class,text,duration,dt_dic,time_,pred):
        st_page=PlotPage_class(parent,self,text,duration,dt_dic,time_,pred)
        st_page.grid(row=0, column=0, sticky="nsew")
        st_page.tkraise()

    def load_README(self):
        #Load txt file to screen
        #from os import startfile
        #startfile("C:/Users/itsba/Desktop/Project/README.txt")
        
        #load new frame contains txt file
        file = open("README.txt").read()
        textframe=tk.Toplevel(self)
        textbox=tk.Label(textframe,text=file)
        textbox.pack(side=tk.LEFT)
        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        controller.geometry(frame_size)
        controller.pack_propagate(0)
        #topFrame
        top_frame=tk.Frame(self,bg='white')
        top_frame.place(x=0,y=0)
        top_frame.pack(fill="both")
        #checking if user exist
        login_text,flag=self.get_user_name()
        
        #login image + button
        self.user_auth=tk.PhotoImage(file='./b_gui/auth_user1.png')
        #login button
        self.login_button=tk.Button(top_frame,fg=login_toplabel_color,command=lambda : controller.show_frame("TwitterLogin"),bg='white')
        self.login_button.config(image=self.user_auth,width="28",height="24",relief=tk.FLAT)
        self.login_button.pack(side=tk.TOP,anchor='ne',pady=1,padx=5)
                        

        #verification label 
        self.verified_label=tk.Label(top_frame,bg='white')
        if flag==True:
            print("True")
            self.verified_label.config(text="Verified",fg='green')
        else:
            self.verified_label.config(text="Autenticate",fg='red')
        self.verified_label.pack(side=tk.TOP,anchor='ne')
        
        
        # ~ MAIN LOGO ~
        self.main_logo=tk.PhotoImage(file='./b_gui/Twitter Prediction1.png')
        self.top_label=tk.Label(top_frame,bg='white')       
        self.top_label.pack(side=tk.TOP)
        self.top_label.config(image=self.main_logo)
        
        
        #Seperator Frame between text and fields
        separator_label_frame=tk.Frame(self)
        separator_label_frame.configure(bg=button_background_color)
        separator_label_frame.pack(fill="both")
        #separator
        self.sep_style=ttk.Style()
        self.sep_style.configure('s.TSeparator')
        separator = ttk.Separator(separator_label_frame, orient='horizontal',style='s.TSeparator')
        separator.pack(side="top",fill='both',padx=15)
        
        
        #images for center frame
        self.insert_hashtag=tk.PhotoImage(file='./b_gui/insert_hashtag.png')
        self.set_duration=tk.PhotoImage(file='./b_gui/set_duration.png')
        self.percentage=tk.PhotoImage(file='./b_gui/percentage.png')

        # ~~ CENTER FRAME ~~
        #MIDDLE MAIN FRAME
        self.centerFrame=tk.Frame(separator_label_frame,bg=button_background_color)
        self.centerFrame.pack(side=tk.TOP,anchor='w',pady=10,padx=10)
        #LABELS FRAME
        self.labelsFrame=tk.Frame(self.centerFrame,bg=button_background_color)
        self.labelsFrame.pack(anchor='nw',pady=10)
        #label insert
        label_h=tk.Label(self.labelsFrame,image=self.insert_hashtag,font=controller.text_font,fg=text_color,bg=button_background_color)
        label_h.pack(side=tk.LEFT,pady=15)
        #TextBox
        self.textbox_h=tk.Entry(self.labelsFrame,bg=button_background_color)
        self.textbox_h.insert(0, 'Any Topic')
        self.textbox_h.bind('<FocusIn>', self.on_entry_click)
        self.textbox_h.bind('<FocusOut>', self.on_focusout)
        self.textbox_h.config(fg = 'black',width=30)
        self.textbox_h.pack(side=tk.LEFT,padx=5)
        #duration FRAME
        self.durationFrame=tk.Frame(self.centerFrame,bg=button_background_color)
        self.durationFrame.pack(anchor='nw',pady=10)
        #label duration
        label_ts=tk.Label(self.durationFrame,image=self.set_duration,font=controller.text_font,fg=text_color,bg=button_background_color,borderwidth=0)
        label_ts.pack(side=tk.LEFT,pady=10)
        #option bar for days selection
        self.time_options={"1 Day":1,"2 Days":2,"3 Days":3,"4 Days":4,"5 Days":5,"6 Days":6,"7 Days":7}
        self.variable=tk.StringVar(self.durationFrame)
        self.variable.set("1 Day")
        option_menu_time=tk.OptionMenu(self.durationFrame,self.variable,*self.time_options.keys())
        option_menu_time["menu"].config(fg=login_toplabel_color,font=controller.text_font,bg=button_background_color)
        option_menu_time.configure(highlightbackground=button_background_color,width = 6,height=1,relief=tk.GROOVE,bg=button_background_color,foreground=login_toplabel_color, activebackground = "#33B5E5")
        option_menu_time.pack(side=tk.RIGHT)
        self.variable.trace("w",self.get_duration)
        duration=(self.variable.get()).split('Day')[0]
        #percentage FRAME
        self.percentageFrame=tk.Frame(self.centerFrame,bg=button_background_color)
        self.percentageFrame.pack(anchor='nw',pady=10)       
        #label percentage
        label_percentage=tk.Label(self.percentageFrame,image=self.percentage,font=controller.text_font,fg=text_color,bg=button_background_color)
        label_percentage.pack(side=tk.LEFT) 
        #Scaler for precentage bar
        self.s_var=tk.DoubleVar()
        self.scale=tk.Scale(self.percentageFrame,variable=self.s_var,orient=tk.HORIZONTAL,from_=5,to=20,tickinterval=5,bg=button_background_color,fg=text_color,troughcolor=login_toplabel_color)
        self.scale.pack(side=tk.LEFT)
        self.scale.config(highlightbackground=button_background_color)
        
        
        # ~ BOTTOM FRAME ~

        self.bottomFrame=tk.Frame(self,bg=button_background_color)
        self.bottomFrame.pack(side=tk.TOP,fill='both')
                
        self.runFrame=tk.Frame(self.bottomFrame,bg=button_background_color)
        self.runFrame.pack(side=tk.RIGHT,padx=20)
        
        #run button
        self.run_img=tk.PhotoImage(file='./b_gui/run2.png')
        self.run_button=tk.Button(self.runFrame,text="Search",fg=text_color,font=controller.text_font,compound="right",command=lambda: self.check_input(parent,self.textbox_h,duration),bg=button_background_color)
        self.run_button.config(image=self.run_img,relief=tk.FLAT)
        if flag==False:
           self.run_button.config(command=lambda: self.user_error_dialog)  
        self.run_button.pack(side=tk.RIGHT,anchor="se",padx=30,fill='both')

        
    #~~~~~CLASS FUNCTIONS~~~~~

    def user_error_dialog(self):
         messagebox.showinfo("Please authentication with twitter developer account.")    
        
    def get_user_percentage(self):
        get_Scale=self.s_var.get()/100
        return get_Scale
    
    def check_input(self,parent,textbox_h,duration):
        scale=self.get_user_percentage()
        if re.match("^[A-Za-z0-9_-]*$", textbox_h.get()):
            self.controller.show_status_frame(parent,StatusPage,textbox_h,duration,scale) 
        else:
            messagebox.showinfo("Information","can only accept a-z ,A-Z,0-9")        
       
    
    def get_duration(self,*args):
        return self.time_options[self.variable.get()]


    def on_entry_click(self,event):
        """function that gets called whenever entry is clicked"""
        if self.textbox_h.get() == 'Any Topic':
            self.textbox_h.delete(0, "end") # delete all the text in the entry
            self.textbox_h.insert(0, '') #Insert blank for user input
            self.textbox_h.config(fg = text_color)
            
    def on_focusout(self,event):
        if self.textbox_h.get() == '':
            self.textbox_h.insert(0, 'Any Topic')
            self.textbox_h.config(fg=text_color)
            
    def get_user_name(self):
        user=DataBase.get_user_name()
        if user!='':
            s="Hello "+user
            return s,True
        else:
            return "Authenticate with Twitter Developer",False
        




class TwitterLogin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        controller.geometry(frame_size)
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
            entry = tk.Entry(row, width=45,bg=button_background_color)
            entries.append(entry)
            row.pack(side="top",fill='both', padx=5, pady=15)
            labels.pack(side="left")
            entry.pack(side="right",padx=3, expand=1, fill='both')
            inputs[field]=entry.get()

                      
        self.verify_acc=tk.Button(twitt_login,text="Verify",bg=button_background_color,fg=login_toplabel_color,command=lambda: self.verify_inputs(entries))
        self.verify_acc.pack(side='right',padx=10,pady=10) 
     
        twitt_login.pack(side="left")

        
        separator = ttk.Separator(self, orient='vertical')
        separator.pack(side="left",fill='both',padx=15,pady=10)
        
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
        
        # if consumer_key==None
        try:
            if len(consumer_key)!=0 and len(consumer_secret)!=0 and len(access_token)!=0 and len(access_token_secret)!=0:
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth, wait_on_rate_limit=True)
               
                #show user name
                user = api.me()
                print("success : ",user.name)
                DataBase.dropTable()
                DataBase.create_connection(user.name,consumer_key,consumer_secret,access_token,access_token_secret)
                print("success adding to db")
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
      

class StatusPage(tk.Frame):
    
    def __init__(self,parent,controller,textbox_h,duration,scale):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.parent=parent    
        self.score_label=0
        self.percentage=scale
   
        #status frame
        self.statusFrame=tk.Frame(self,bg='white')
        self.statusFrame.pack(fill='both',side=tk.TOP,anchor="center")
        #label status
        self.processing_img=tk.PhotoImage(file='./b_gui/processing.png')
        self.label_status=tk.Label(self.statusFrame,image=self.processing_img)
        self.label_status.pack(side=tk.TOP,pady=10,anchor="center")
        
        #center Frame
        self.centerFrame=tk.Frame(self,bg='white')
        self.centerFrame.pack(anchor='center',pady=5,fill='both')
        #time label
        self.var = tk.StringVar()
        self.var.set('Time left for fetching tweets:')
        self.time_label=tk.Label(self.centerFrame,textvariable=self.var,bg='white')
        self.time_label.pack(side=tk.TOP)                
        #progress bar
        self.progressBar =ttk.Progressbar(self.centerFrame,orient="horizontal",style="red.Horizontal.TProgressbar",length=400,  mode="determinate")
        self.progressBar.pack(side=tk.TOP)
        self.input_=textbox_h.get()
        
        #center Frame2
        self.center_Frame2=tk.Frame(self,bg='white')
        self.center_Frame2.pack(side=tk.TOP)
        
        #informationFrame
        self.informationFrame=tk.LabelFrame(self.center_Frame2,text='Information',width=400, height=200)
        self.informationFrame.pack(anchor='w')
        self.centerInfoFrame=tk.Frame(self.informationFrame)
        self.centerInfoFrame.pack()
    
        texts_for_labels='Fetching Tweets','Preprocess Tweets','Sentiment Analysis','LSTM Prediction'
        self.checkboxes={}
        self.checkbox_fetchs_tweets={}
        self.update_information={}
        for text_l in texts_for_labels:
            row_frame = tk.Frame(self.centerInfoFrame)
            process_label=tk.Label(row_frame,text=text_l,fg=text_color,width=20)
            process_label.pack(side=tk.LEFT)
           
            self.checkboxes[text_l]=tk.Variable()
            checkbox_fetch_tweets=tk.Checkbutton(row_frame,selectcolor='green',state=tk.DISABLED,variable=self.checkboxes[text_l])
            row_frame.pack(side="top",fill='both', padx=15, pady=10)
            
            checkbox_fetch_tweets.pack(side=tk.LEFT)
            checkbox_fetch_tweets.deselect()
            self.checkbox_fetchs_tweets[text_l]=checkbox_fetch_tweets
            
            self.v = tk.StringVar()
            update_process_label=tk.Label(row_frame,textvariable=self.v,fg=text_color,width=20)
            self.update_information[text_l]=self.v
            update_process_label.pack(side=tk.LEFT)



        self.information_update=tk.Label(self,text="")
        self.preprocessed_amount=0
     
        self.informationFrame.pack(side=tk.LEFT)
        
        #Buttom frame
        self.buttomFrame=tk.Frame(self,bg='white')
        self.buttomFrame.pack(fill='both',side=tk.TOP,anchor="n")
        #Cancel button
        self.cancel_button=tk.Button(self.buttomFrame,fg=text_color,text="Cancel",command=lambda:controller.destroy(),bg=button_background_color)
        self.cancel_button.configure(width = 10, activebackground = "#33B5E5", relief = tk.FLAT)
        self.cancel_button.pack(padx=10,pady=5,side=tk.RIGHT) 
        
        
        #start thread 
        self.start_submit_thread(self.input_,duration,True,controller)
    

    def load_score_of_ml(self):
        try:
            filename = './pickle/sentiment_score.txt'
            with open(filename,'r') as textfile:
                 score=textfile.read()
                 
            return score
           
        except (FileNotFoundError ,IOError):
            print("Error loading file")
            return 0
    
    
    def start_submit_thread(self,TEXT,duration,flag,master):
        global submit_thread
        global lock
        lock=threading.Lock()
        submit_thread = threading.Thread(target=lambda :self.run(TEXT,duration,flag,master))
        submit_thread.daemon = True
        submit_thread.start()
        
   
    def run(self,text,duration,flag,master):
        duration=int(duration)
        try:
            #lock.acquire()
        
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
                for i in range(1):
                    print("Fetch number : ",(i+1),'/',hours)
                    TweetCon.runTweetCon(text,0)
                    self.progressBar['value']+=10     
                    self.var.set('Time left: {} Hours'.format(hours-i))
                    time.sleep(1)
                
                self.checkbox_fetchs_tweets['Fetching Tweets'].select()
                self.size_of_fetching_tweets=util. get_size_of_file("./csvData/"+text+"/"+text+"_hashtag_tweets.csv")
                self.update_information['Fetching Tweets'].set(str(self.size_of_fetching_tweets)+" tweets fetched")
                self.var.set('')
                time.sleep(3)
                #run preprocess
                preprocess.runPreprocess(2,text)
                self.progressBar['value']+=20
                self.checkbox_fetchs_tweets['Preprocess Tweets'].select()
                self.size_of_preprocessing=util. get_size_of_file("./csvData/"+text+"/preprocess_"+text+"_hashtag_tweets.csv")
                self.update_information['Preprocess Tweets'].set(str(self.size_of_preprocessing)+" tweets preprocess")
                time.sleep(3)
                
                #run npl 
                NLP.run_natural_language_processing(text,True)
                self.progressBar['value']+=20
                self.checkbox_fetchs_tweets['Sentiment Analysis'].select()
                
                #getting ml score
                self.score_label=self.load_score_of_ml()
                self.update_information['Sentiment Analysis'].set(self.score_label+"% accuracy")
                time.sleep(3)


                timeSeries.run_time_series(text,True)
                
                print("start lstm")
                dt_dic,time_,pred=LSTM_ver2.main_pred("Trump",self.percentage)
                self.progressBar['value']+=20
                self.checkbox_fetchs_tweets['LSTM Prediction'].select()
                
               
                self.controller.show_plots_frame(self.parent,PlotPage,text,duration,dt_dic,time_,pred)
                #result_page(text,date_time_dic)
            #else:   
                #date_time_dic=timeSeries.run_time_series('',False)
                #result_page('',date_time_dic)
                
           # lock.release()
                  
        except KeyboardInterrupt as err:
            print(err)
            

class PlotPage(tk.Frame):
       
    def __init__(self,parent,controller,text,duration,dt_dic,time_,pred):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.text=text
        controller.geometry("820x560")
        
        #top frame
        self.topFrame=tk.Frame(self)
        self.topFrame.pack(side=tk.TOP,fill='both')
        #back button
        self.back_button=tk.Button(self.topFrame,fg=text_color,text="Back",command=lambda:self.controller.show_frame("StartPage"),bg=button_background_color)
        self.back_button.configure(width = 10, activebackground = "#33B5E5", relief = tk.GROOVE)
        self.back_button.pack(padx=15,pady=5,anchor="nw")


        #~NOTEBOOK~
        self.notebook=ttk.Notebook(self)
        #prediction frame
        self.prediction_frame=ttk.Frame(self.notebook)
        self.loss_val_frame=ttk.Frame(self.notebook)
        self.notebook.add(self.prediction_frame, text='Prediction Plots')
        self.notebook.add(self.loss_val_frame, text='Validation/Loss Plots')
        self.notebook.pack(anchor="c",fill='both',padx=15,pady=5)


        #Button Images
        self.previousPhoto=tk.PhotoImage(file='./b_gui/back.png')
        self.nextPhoto=tk.PhotoImage(file='./b_gui/next.png')
        
        #plot frame - PREDICTIONS
        
        #uploading plots images
        self.plots_images=self.upload_plots(dt_dic,time_,pred,text)
        self.count=0
        #Left page-left button
        self.left_button=tk.Button(self.prediction_frame,text="",state=tk.DISABLED,command=lambda : self.switch_prev__plot())
        self.left_button.pack(side=tk.LEFT)      
        #right page- right button
        self.right_button=tk.Button(self.prediction_frame,text="",command=lambda : self.switch_next__plot())
        self.right_button.pack(side=tk.RIGHT)
        self.left_button.config(image=self.previousPhoto,width="64",height="64",relief=tk.FLAT)
        self.right_button.config(image=self.nextPhoto,width="64",height="64",relief=tk.FLAT)
        #center page-Plot label
        self.plot_label=tk.Label(self.prediction_frame,image=self.plots_images[self.count])
        self.plot_label.pack(anchor='center',padx=25,pady=5) 
        #. 
        
        
        #VALIDATION / LOSS frame
        
        #uploading plots images
        self.plots_images1=self.upload_loss(text)
        self.count1=0
        #Left page-left button
        self.left_button1=tk.Button(self.loss_val_frame,state=tk.DISABLED,command=lambda : self.switch_prev__plot1())
        self.left_button1.pack(side=tk.LEFT)      
        #right page- right button
        self.right_button1=tk.Button(self.loss_val_frame,command=lambda : self.switch_next__plot1())
        self.right_button1.pack(side=tk.RIGHT)
        self.left_button1.config(image=self.previousPhoto,width="64",height="64",relief=tk.FLAT)
        self.right_button1.config(image=self.nextPhoto,width="64",height="64",relief=tk.FLAT)
        #center page-Plot label
        self.plot_label1=tk.Label(self.loss_val_frame,image=self.plots_images1[self.count1])
        self.plot_label1.pack(anchor='center',padx=25,pady=5) 
        
        #informationFrame
        self.informationFrame=tk.LabelFrame(self,text='Information')
        self.informationFrame.pack(side=tk.TOP,fill='both',padx=50)
        #center information frame
        self.centerInfoFrame=tk.Frame(self.informationFrame,width=600, height=300)
        self.centerInfoFrame.pack(anchor='center')
        #reading file 
        file='csvData/'+self.text+'/predict_'+self.text+'_hashtag_tweets.csv'
        read_file=pd.read_csv(file)
        
        
        #font
        info_font=tk.font.Font(family='Verdana', size=8, weight="bold")
        #Inserting data into information frame
        self.count_pos=read_file['count_pos'].sum()
        self.count_neg=read_file['count_neg'].sum()
        self.average=read_file['average'].mean()
        self.count_pos_label=tk.Label(self.centerInfoFrame,text="Total Positive Tweets: "+str(int(self.count_pos)),fg=text_color,font=info_font)
        self.count_neg_label=tk.Label(self.centerInfoFrame,text="Total Negative Tweets: "+str(int(self.count_neg)),fg=text_color,font=info_font)
        self.count_pos_label.pack(anchor="nw")
        self.count_neg_label.pack(anchor="nw")
        self.average_label=tk.Label(self.centerInfoFrame,text="Average score: "+str(round(self.average,2)),fg=text_color,font=info_font)
        self.average_label.pack(anchor="nw")
        
        #eqFont=tk.font.Font(bold,size=8)
        self.function_label=tk.Label(self.centerInfoFrame,text='Formula for computing each hour: ( ∑ Positive - ∑ Negative ) / Total',fg=text_color,font=info_font)
        self.function_label.pack(anchor="ne",pady=5)
        
    #FOR PREDICTION PLOTS
    def switch_next__plot(self):
        #switch to next date plot
        plots_len=len(self.plots_images)
        if self.count<plots_len:
           self.count+=1
        self.left_button['state']=tk.NORMAL
        print("Switch to the next plot")
        if self.count<plots_len:
            self.plot_label.configure(image=self.plots_images[self.count])     
            self.plot_label.pack(anchor='center',padx=15,pady=5)
        elif self.count==plots_len:        
            self.right_button['state']=tk.DISABLED
                 
    def switch_prev__plot(self):
    #switch to previous date plot
       plots_len=len(self.plots_images)
       if self.count==plots_len:
          self.right_button['state']=tk.NORMAL
       self.count-=1
       if self.count!=0:
           self.plot_label.configure(image=self.plots_images[self.count])     
           self.plot_label.pack(anchor='center',padx=15,pady=5)
       if self.count==0:
           self.plot_label.configure(image=self.plots_images[self.count])
           self.left_button['state']=tk.DISABLED
    
    
    # FOR VAL -LOSS PLOTS
    def switch_next__plot1(self):
        #switch to next date plot
        plots_len=len(self.plots_images1)
        if self.count1<plots_len:
           self.count1+=1
        self.left_button1['state']=tk.NORMAL
        print("Switch to the next plot")
        if self.count1<plots_len:
            self.plot_label1.configure(image=self.plots_images1[self.count1])     
            self.plot_label1.pack(anchor='center',padx=15,pady=5)
        elif self.count1==plots_len:        
            self.right_button1['state']=tk.DISABLED
            
    def switch_prev__plot1(self):
    #switch to previous date plot
       plots_len=len(self.plots_images1)
       if self.count1==plots_len:
          self.right_button1['state']=tk.NORMAL
       self.count1-=1
       if self.count1!=0:
           self.plot_label1.configure(image=self.plots_images1[self.count1])     
           self.plot_label1.pack(anchor='center',padx=15,pady=5)
       if self.count1==0:
           self.plot_label1.configure(image=self.plots_images1[self.count1])
           self.left_button1['state']=tk.DISABLED
    
    
    def upload_plots(self,dt_dic,time_,pred,text):    
         '''takes each plot and add to an array '''
         #array of label
         plots_labels =[]
    
         count_plots=[]
         #Plotting graphs by Date and Hours 
         for i in range(len(dt_dic)):
             count_plots.append(i)
         
         print("count_plots= ",count_plots)
         count=0
         for key,value in dt_dic.items():
             self.text='Trump'
            
             self.image_path='./csvData/'+self.text+'/plots/'+self.text+'_plot_'+key+'.png'
             plots_labels.append(tk.PhotoImage(file=self.image_path))
             count+=1
         image_path_pred='./csvData/'+self.text+'/plots/'+self.text+'_prediction_plot.png'
         plots_labels.append(tk.PhotoImage(file=image_path_pred))
         
         return plots_labels
     
        
        
    def upload_loss(self,text):    
         '''takes each plot and add to an array '''
         #array of label
         plots_labels =[]
    
         for index in range(1,13):
             self.text='Trump'
            
             self.image_path='./csvData/'+self.text+'/plots/'+self.text+'_loss_plot_'+str(index)+'.png'
             plots_labels.append(tk.PhotoImage(file=self.image_path))
         
         return plots_labels
     

     
             
    def open_canvas(self,plots_labels,count):
        self.text='Trump'
        plots_labels.images
        plots_labels.config(image=plots_labels.images[count])
        plots_labels.pack()
          
                            

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()