#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 01:07:19 2019

@author: yaron
"""


frame_size="640x550"
backround_color='white'
text_color='#3d3d3d'
login_toplabel_color='#3898DB'
button_background_color='#E7EDF1'

import matplotlib
matplotlib.use('Agg')
import pandas as pd
from pathlib import Path
import TweetCon 
import NLP
import preprocess 
import timeSeries
import LSTM
import utility as util
from importlib import reload  # Python 3.4+ only.
import threading
import time
import re

import tweepy
import DataBase

LSTM=reload(LSTM)
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
        self.text_font = tkfont.Font(family='Verdana', size=10, weight="bold")

        self.geometry(frame_size)

        self.resizable(False,False)

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
        
    #raising StartPage or TwitterLogin
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    
    #raising StatusPage     
    def show_status_frame(self,parent,status_class,text,duration):
        st_page=status_class(parent,self,text,duration)
        st_page.grid(row=0, column=0, sticky="nsew")
        st_page.tkraise()
        
    #raising PlotPage    
    def show_plots_frame(self,parent,PlotPage_class,text,duration,dt_dic,time_,pred):
        st_page=PlotPage_class(parent,self,text,duration,dt_dic,time_,pred)
        st_page.grid(row=0, column=0, sticky="nsew")
        st_page.tkraise()

    #rasing LstmPage
    def show_lstm_frame(self,parent,LstmPage_class,text,duration):
        lstm_page=LstmPage_class(parent,self,text,duration)
        lstm_page.grid(row=0, column=0, sticky="nsew")
        lstm_page.tkraise()
        
    #README
    def load_README(self):
        #load new frame contains txt file
        file = open("README.txt").read()
        textframe=tk.Toplevel(self)
        textbox=tk.Label(textframe,text=file)
        textbox.pack(side=tk.LEFT)


##### START PAGE #####        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent=parent
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
            self.verified_label.config(text="Verified",fg='green')
        else:
            self.verified_label.config(text="Autenticate",fg='red')
        self.verified_label.pack(side=tk.TOP,anchor='ne')
        
        
        # ~ MAIN LOGO ~
        self.main_logo=tk.PhotoImage(file='./b_gui/Twitter Prediction3.png')
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
        separator.pack(side="top",fill='both')
        
        
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
        self.textbox_h=tk.Entry(self.labelsFrame,bg='white')
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
       
        
        #percentage FRAME
        self.percentageFrame=tk.Frame(self.centerFrame,bg=button_background_color)
        self.percentageFrame.pack(anchor='nw',pady=10)       
  
        
        
        # ~ BOTTOM FRAME ~
        self.bottomFrame=tk.Frame(self,bg=button_background_color)
        self.bottomFrame.pack(side=tk.TOP,fill='both')
                
        self.runFrame=tk.Frame(self.bottomFrame,bg=button_background_color)
        self.runFrame.pack(side=tk.RIGHT,padx=20)
        
        #run button
        self.run_img=tk.PhotoImage(file='./b_gui/run2.png')
        self.run_button=tk.Button(self.runFrame,text="Search",fg=text_color,font=controller.text_font,compound="right",command=lambda: self.check_input(parent,self.textbox_h),bg=button_background_color)
        self.run_button.config(image=self.run_img,relief=tk.FLAT)
        #if Authentication failed
        if flag==False:
           self.run_button.config(command=lambda: self.user_error_dialog)  
        self.run_button.pack(side=tk.RIGHT,anchor="se",padx=30,fill='both')


        #separator
        self.sep_style=ttk.Style()
        self.sep_style.configure('s.TSeparator')
        separator = ttk.Separator(self, orient='horizontal',style='s.TSeparator')
        separator.pack(side="top",fill='both')
        
        
        #LstmFrame
        self.lstmFrame=tk.Frame(self,bg='white')
        self.lstmFrame.pack(side=tk.BOTTOM,fill='both')
        
        #lstm label
        self.or_image=tk.PhotoImage(file='./b_gui/or_label.png')
        self.lstmLabel=tk.Label(self.lstmFrame,image=self.or_image,highlightthickness=0,borderwidth=0)
        self.lstmLabel.pack(side=tk.TOP)
    
        #Lstm button
        self.run_lstm_image=tk.PhotoImage(file='./b_gui/run_lstm_only.png')
        self.lstmButton=tk.Button(self.lstmFrame,image=self.run_lstm_image,command=lambda:self.check_input_lstm(),relief=tk.FLAT)
        self.lstmButton.pack(side=tk.BOTTOM,pady=10)
        
        
        self.configure(background='white')
        
        
    #~~~~~CLASS FUNCTIONS~~~~~

    
    def user_error_dialog(self):
         messagebox.showinfo("Please authentication with twitter developer account.")    
        
  
    
    
    def check_input_lstm(self):
        text=self.textbox_h.get()
        file_to_read="./csvData/"+text+"/predict_"+text+"_hashtag_tweets.csv"
        file=Path(file_to_read)
        
        if re.match("^[A-Za-z0-9_-]*$", text):
                if file.exists():
                    self.controller.show_lstm_frame(self.parent,LstmPage,text,0)
                else:
                    messagebox.showinfo("Information","csv file not exist") 
                    
        else:
            messagebox.showinfo("Information","can only accept a-z ,A-Z,0-9")   
            
            
            
            
    def check_input(self,parent,textbox_h):
        duration=self.variable.get().split('Day')[0]
        print("duration=",duration)
        if re.match("^[A-Za-z0-9_-]*$", textbox_h.get()):
            self.controller.show_status_frame(parent,StatusPage,textbox_h,duration) 
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
        



##### Twitter Login #####
class TwitterLogin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        controller.geometry(frame_size)
        
        #button Back to StartPage
        self.back_img=tk.PhotoImage(file='./b_gui/back_page.png')
        button = tk.Button(self, image=self.back_img,command=lambda: controller.show_frame("StartPage"),relief=tk.FLAT)
        button.pack(anchor="w",padx=7)
        
        #authentication Label
        self.auth_img=tk.PhotoImage(file='./b_gui/auth.png')
        login_label=tk.Label(self,image=self.auth_img,bg='white',font=controller.title_font)
        login_label.pack(anchor="n",fill="x",pady=2)
        self.cons_key=""
        self.configure(bg='white')
        
        #frame label images
        self.con_key_img=tk.PhotoImage(file='./b_gui/con_key.png')
        self.con_sec_img=tk.PhotoImage(file='./b_gui/con_sec.png')
        self.con_acctoken_img=tk.PhotoImage(file='./b_gui/con_acctoken.png')
        self.con_acctokensecret_img=tk.PhotoImage(file='./b_gui/con_acctoken_secret.png')
        
        #TwitterLogin Frame
        twitt_login=tk.Frame(self,bg='white')
        twitt_login.pack(side=tk.TOP,anchor='w',pady=10)
 
        fields=[self.con_key_img,self.con_sec_img,self.con_acctoken_img,self.con_acctokensecret_img]
        inputs = {}
        entries=[]
        for field in fields:
            row = tk.Frame(twitt_login,bg='white')
            labels = tk.Label(row, image=field, anchor='w',fg=text_color,bg='white')
            entry = tk.Entry(row, width=60,bg='white')
            entries.append(entry)
            row.pack(side=tk.TOP, padx=5, pady=5)
            labels.pack(side=tk.LEFT)
            self.config(bg='white')
            entry.pack(side=tk.RIGHT,padx=3, expand=1)
            inputs[field]=entry.get()
            
        #Verify Button    
        self.verify_img=tk.PhotoImage(file='./b_gui/verify.png')
        buttonFrame=tk.Frame(self)
        buttonFrame.pack(side=tk.TOP,anchor="n")
        self.verify_acc=tk.Button(buttonFrame,image=self.verify_img,bg='white',command=lambda: self.verify_inputs(entries),relief=tk.FLAT)
        self.verify_acc.pack(side=tk.LEFT,anchor='w') 
        #Seperator        
        self.dots_Sep=tk.PhotoImage(file='./b_gui/seperator1.png')
        self.dot_label=tk.Label(self,image=self.dots_Sep,bg='white').pack(side=tk.TOP,fill='both')
        #infoFrame
        info_frame=tk.Frame(self,bg='white')
        info_frame.pack(side=tk.TOP,anchor="w")
        self.guidance_img=tk.PhotoImage(file='./b_gui/guidance2.png')
        label_guidance=tk.Label(info_frame,image=self.guidance_img,borderwidth=0,highlightthickness = 0)
        label_guidance.pack(side=tk.LEFT,padx=3)
        
  
    ####### CLASS FUNCTION #######
            
    def verify_inputs(self,entries):
        
        #inputs received from entries 
        consumer_key=entries[0].get()
        consumer_secret=entries[1].get()
        access_token=entries[2].get()
        access_token_secret=entries[3].get()
     
        
        #Authentication With Twitter Developer Account        
        try:
            if len(consumer_key)!=0 and len(consumer_secret)!=0 and len(access_token)!=0 and len(access_token_secret)!=0:
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth, wait_on_rate_limit=True)
               
                #create connection to db and add username
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
      


##### StatusPage #####
class StatusPage(tk.Frame):
    
    def __init__(self,parent,controller,textbox_h,duration):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.parent=parent    
        self.score_label=0
        self.twitter_flag=0
      


        #status frame
        self.statusFrame=tk.Frame(self,bg='white')
        self.statusFrame.pack(fill='both',side=tk.TOP,anchor="center")
        #label status
        self.processing_img=tk.PhotoImage(file='./b_gui/processing.png')
        self.label_status=tk.Label(self.statusFrame,image=self.processing_img,highlightbackground='white',borderwidth=0)
        self.label_status.pack(side=tk.TOP,pady=10,anchor="center")
        #center Frame
        self.centerFrame=tk.Frame(self,bg='white')
        self.centerFrame.pack(anchor='center',fill='both')
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
        self.center_Frame2.pack(side=tk.TOP,pady=10)
        
        #informationFrame
        self.informationFrame=tk.LabelFrame(self.center_Frame2,text='Information',width=400, height=200,bg='white')
        self.informationFrame.pack(anchor='w')
        self.centerInfoFrame=tk.Frame(self.informationFrame,bg='white')
        self.centerInfoFrame.pack()
    
        ####
        #frame label images
        self.fetching_tweets=tk.PhotoImage(file='./b_gui/fetching_tweets.png')
        self.preprocessing_tweets=tk.PhotoImage(file='./b_gui/preprocessing_tweets.png')
        self.sentiment_analysis=tk.PhotoImage(file='./b_gui/sentiment_analysis.png')
        #self.lstm_prediction=tk.PhotoImage(file='./b_gui/lstm_prediction.png')
        
        #Info frame with labels
        texts_for_labels=[self.fetching_tweets,self.preprocessing_tweets,self.sentiment_analysis]
        self.checkboxes={}
        self.checkbox_fetchs_tweets={}
        self.update_information={}

        for text_l in texts_for_labels:
            row_frame = tk.Frame(self.centerInfoFrame)
            row_frame.config(bg='white')
            process_label=tk.Label(row_frame,image=text_l,bg='white')
            process_label.pack(side=tk.LEFT)
            self.checkboxes[text_l]=tk.Variable()
            checkbox_fetch_tweets=tk.Checkbutton(row_frame,selectcolor='green',state=tk.DISABLED,variable=self.checkboxes[text_l],bg='white')
            row_frame.pack(side="top",fill='both', padx=10, pady=10)
            
            checkbox_fetch_tweets.pack(side=tk.LEFT)
            checkbox_fetch_tweets.deselect()
            self.checkbox_fetchs_tweets[text_l]=checkbox_fetch_tweets
            
            self.v = tk.StringVar()
            update_process_label=tk.Label(row_frame,textvariable=self.v,fg=text_color,width=20,bg='white')
            self.update_information[text_l]=self.v
            update_process_label.pack(side=tk.LEFT)


        self.configure(bg='white')
        
        #start thread 
        #self.run(self.input_,duration,True,controller)
        self.start_submit_thread(self.input_,duration,True,controller)
           
     
        
       

    
####### CLASS FUNCTIONS #######

    #loading score of Linear Machine
    def load_score_of_ml(self):
        try:
            filename = './pickle/sentiment_score.txt'
            with open(filename,'r') as textfile:
                 score=textfile.read()
     
            return score
           
        except (FileNotFoundError ,IOError):
            print("Error loading file")
            return 0
    
    def check_if_ready(self,thread,text,duration):
        if thread.is_alive():
            self.after(1000,self.check_if_ready,thread,text,duration)
        else:
            if self.twitter_flag==1:
               messagebox.showerror("Error","Tweets not found")
               self.controller.show_frame("StartPage")
            else:
                print("lstm thread done\n")
                self.controller.show_lstm_frame(self.parent,LstmPage,text,duration)
            
    
    #Starting theding to run all the PROCESSES
    def start_submit_thread(self,TEXT,duration,flag,master):
        global submit_thread
        global lock
        lock=threading.Lock()
        submit_thread = threading.Thread(target=lambda :self.run(TEXT,duration,flag,master))
       # submit_thread.daemon = True
        submit_thread.start()
        self.after(1000,self.check_if_ready,submit_thread,TEXT,int(duration))
        
     
       
        
    # MAIN RUN OF ALL PROCESSES #
    def run(self,text,duration,flag,master):
        duration=int(duration)
        print("\nduration=",duration)
        
        try:
            #lock.acquire()
        
            #connection to twitter and fetching tweets
            hours=duration*24
            print("Processing hours : ",hours)
            #progressbar
            p_size=(hours*10)+60
            self.progressBar['maximum']=p_size
            self.var.set('Time left: Processing...')

            #loop for fetching tweet by hours
            for i in range(hours): 
                print("Fetch number : ",(i+1),'/',hours)
                size_of_hashtag=TweetCon.runTweetCon(text,0)
                if size_of_hashtag==0:
                    self.twitter_flag=1
                    return 
                    
                self.progressBar['value']+=10     
                self.var.set('Time left: {} Hours'.format(hours-i))
                time.sleep(60*60)
                
            self.checkbox_fetchs_tweets[self.fetching_tweets].select()
            self.size_of_fetching_tweets=util. get_size_of_file("./csvData/"+text+"/"+text+"_hashtag_tweets.csv")
            self.update_information[self.fetching_tweets].set(str(self.size_of_fetching_tweets)+" tweets fetched")
            self.var.set('')
            time.sleep(3)
            
            #run preprocess 
            #1=preprocess dataSet,2=preprocess to hashtag Tweets ,3=divide dataset by size 
            preprocess.runPreprocess(2,text)
            self.progressBar['value']+=20
            self.checkbox_fetchs_tweets[self.preprocessing_tweets].select()
            self.size_of_preprocessing=util. get_size_of_file("./csvData/"+text+"/preprocess_"+text+"_hashtag_tweets.csv")
            self.update_information[self.preprocessing_tweets].set(str(self.size_of_preprocessing)+" tweets preprocess")

            time.sleep(3)
                
            #run npl 
            #hashtag and True:using pickle ,False:training and predictiing using ML kfolds LinearSVM    
            NLP.run_natural_language_processing(text)
            self.progressBar['value']+=20
            self.checkbox_fetchs_tweets[self.sentiment_analysis].select()
                
            #getting ML score
            self.score_label=self.load_score_of_ml()
            self.update_information[self.sentiment_analysis].set(self.score_label+"% accuracy")
            
                
 
                
           # lock.release()
        
        except KeyboardInterrupt as err:
            print(err)
            
##### PLOTPAGE #####
class PlotPage(tk.Frame):
       
    def __init__(self,parent,controller,text,duration,dt_dic,pred,size_of_prediction):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.text=text
        self.size_of_prediction=size_of_prediction
        
        controller.geometry("820x560")
        #top frame
        self.topFrame=tk.Frame(self)
        self.topFrame.pack(side=tk.TOP,fill='both')
        #back button

        self.back_button=tk.Button(self.topFrame,fg=text_color,text="Back",command=lambda:self.controller.show_lstm_frame(parent,LstmPage,text,duration),bg=button_background_color)
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
        self.plots_images=self.upload_plots(dt_dic,pred,text)
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
        
    ##### CLASS FUNCTIONS #####    
        
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
            
    #switch to previous date plot
    def switch_prev__plot(self):
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
            
            
    #switch to previous date plot        
    def switch_prev__plot1(self):
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
    
    
    def upload_plots(self,dt_dic,pred,text):    
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
        if self.size_of_prediction>1:
            for index in range(1,self.size_of_prediction):
                 
                self.image_path='./csvData/'+self.text+'/plots/'+self.text+'_loss_plot_'+str(index)+'.png'
                plots_labels.append(tk.PhotoImage(file=self.image_path))
        else:
            self.image_path='./csvData/'+self.text+'/plots/'+self.text+'_loss_plot_'+str(1)+'.png'
            plots_labels.append(tk.PhotoImage(file=self.image_path))
            
        return plots_labels
    
   
     


##### CLASS LstmPage ######
class LstmPage(tk.Frame):   
    def __init__(self,parent,controller,text,duration):
        tk.Frame.__init__(self,parent)
        self.text=text
        self.duration=duration
        self.controller=controller
        self.parent=parent
        
        self.dt_dic=[]
        self.pred=[]
        self.size_of_prediction=0
        
    
      
        #top frame
        self.topFrame=tk.Frame(self,bg='white')
        self.topFrame.pack(side=tk.TOP,fill='both')
        #back button
        self.back_button=tk.Button(self.topFrame,fg=text_color,text="Back",command=lambda:self.controller.show_frame("StartPage"),bg=button_background_color)
        self.back_button.configure(width = 10, activebackground = "#33B5E5", relief = tk.GROOVE)
        self.back_button.pack(padx=15,pady=5,anchor="nw")
        
        #lstm label
        self.lstm_title_image=tk.PhotoImage(file='./b_gui/lstm_prediction1.png')
        self.lstmLabel=tk.Label(self.topFrame,image=self.lstm_title_image,borderwidth=0,highlightthickness=0)
        self.lstmLabel.pack(side=tk.TOP,pady=10,anchor="center")

        #center Frame
        self.centerFrame=tk.Frame(self,bg=button_background_color)
        self.centerFrame.pack(anchor='center',fill='both')
        
     
        
        #smoothFrame
        self.smoothFrame=tk.Frame(self.centerFrame,bg=button_background_color)
        self.smoothFrame.pack(anchor='nw',pady=20)
        self.smooth_image=tk.PhotoImage(file='./b_gui/stationary_data.png')
        #smooth label
        self.smoothLabel=tk.Label(self.smoothFrame,image=self.smooth_image,bg=button_background_color)
        self.smoothLabel.pack(side=tk.LEFT,padx=5)
        #checkButton
        self.smooth_var=tk.IntVar()
        self.checkb_smooth=tk.Checkbutton(self.smoothFrame,variable=self.smooth_var,bg=button_background_color)
        self.checkb_smooth.pack(side=tk.LEFT,padx=2)
        self.checkb_smooth.config(highlightbackground=button_background_color)
        
        #percentage FRAME
        self.percentage_image=tk.PhotoImage(file='./b_gui/percentage_2.png')

        self.percentageFrame=tk.Frame(self.centerFrame,bg=button_background_color)
        self.percentageFrame.pack(anchor='nw',pady=20)       
        #label percentage
        self.label_percentage=tk.Label(self.percentageFrame,image=self.percentage_image,font=controller.text_font,fg=text_color,bg=button_background_color)
        #self.label_percentage.config(image=self.percentage_image)
        self.label_percentage.pack(side=tk.LEFT)
        
        #Scaler for precentage bar
        self.s_var=tk.DoubleVar()
        self.scale=tk.Scale(self.percentageFrame,variable=self.s_var,orient=tk.HORIZONTAL,from_=5,to=20,tickinterval=5,bg=button_background_color,fg=text_color,troughcolor=login_toplabel_color)
        self.scale.pack(side=tk.LEFT)
        self.scale.config(highlightbackground=button_background_color)
        
        #progress bar
        self.progressBar =ttk.Progressbar(self.centerFrame,orient="horizontal",style="red.Horizontal.TProgressbar",length=600,  mode="determinate")
        self.progressBar.pack(side=tk.TOP)

        #bottomFrame
        self.bottomFrame=tk.Frame(self,bg='white')
        self.bottomFrame.pack(side=tk.BOTTOM,fill='both')
        
      

        #run button
        self.run_img=tk.PhotoImage(file='./b_gui/start.png')
        self.runButton=tk.Button(self.bottomFrame,bg='white',image=self.run_img,command=lambda:self.submit_thread(),relief=tk.FLAT)
        self.runButton.pack(side=tk.TOP,anchor="center",pady=50,padx=30)
        self.runButton.config(state="normal")
        
    ####### CLASS FUNCTIONS #######    
        
    def get_checkb_smooth(self):
       var=self.smooth_var.get()

       if(var==0):
           return False
       elif(var==1):
           return True
   
    def get_percentage(self):
        return self.scale.get()
    
    def check_if_ready(self,thread):
        if thread.is_alive():
            self.after(600,self.check_if_ready,thread)
        else:
            print("lstm thread done\n")
            self.controller.show_plots_frame(self.parent,PlotPage,self.text,self.duration,self.dt_dic,self.pred,self.size_of_prediction)
            
        
    def submit_thread(self):
        print("start lstm thread")
        self.runButton.config(state="disabled")
        global submit_thread
        global lock
        lock=threading.Lock()
        smooth_flag=self.get_checkb_smooth()
        percentage=self.get_percentage()
        text=self.text
        submit_thread_ = threading.Thread(target=lambda :self.runLstm(text,smooth_flag,percentage))
   
        submit_thread_.start()
        self.after(600,self.check_if_ready,submit_thread_)
        
        
    def runLstm(self,text,smooth_flag,percentage):
        
        try:
            
            self.progressBar['maximum']=100
        
            percentage=percentage/100
            #timeSeries
           
        
            timeSeries.run_time_series(text,smooth_flag)
            time.sleep(3)
            lock.acquire()
            #LSTM
            #returns date and time dictionary(dt_dic),predictions(pred) and size of prediction
            dt_dic,pred,size_of_prediction=LSTM.main_pred(text,percentage,self.progressBar)
            lock.release()
            
            self.dt_dic=dt_dic
            self.pred=pred
            self.size_of_prediction=size_of_prediction
                
            return
        except:
            print("Error on Lstm !\n")
            self.progressBar['value']=0
            messagebox.showerror("error","Error in lstm ,please try again")

            return
        
        
    
                            

if __name__ == "__main__":
    app = SampleApp()
    app.title("Twitter Predicition Based on Sentiment Analysis" )
    app.mainloop()