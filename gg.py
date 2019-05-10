# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 13:55:56 2019

@author: itsba
"""
import TweetCon 
import NLP
import preprocess 
import timeSeries 
import natural_language_processing
import utility
from importlib import reload  # Python 3.4+ only.
import threading
from tkinter import *
from tkinter.ttk import Progressbar

NLP=reload(NLP)
TweetCon=reload(TweetCon)
preprocess=reload(preprocess)
timeSeries=reload(timeSeries)
reload(natural_language_processing)



def start_submit_thread(TEXT,duration,flag):
    global submit_thread
    global lock
    lock=threading.Lock()
    submit_thread = threading.Thread(target=lambda : run(TEXT,duration,flag))
    submit_thread.daemon = True
    submit_thread.start()


def run(text,duration,flag):
    try:
        lock.acquire()
        
        if(flag==True):
            TweetCon.runTweetCon(text,duration)
            preprocess.runPreprocess(2,text)
            NLP.run_natural_language_processing(text,False)
            date_time_dic=timeSeries.run_time_series(text,True)
            result_page(text,date_time_dic)
        else:   
            date_time_dic=timeSeries.run_time_series('',False)
            result_page('',date_time_dic)
            
        lock.release()
    except KeyboardInterrupt as err:
        print(err)
    

                  
def get_duration(*args):
    return time_options[variable.get()]
               
               
root=Tk()
root.title("PredicTwitter")
root.geometry("500x350")

#TOP FRAME#
topframe=Frame(root)
topframe.pack()
label_h=Label(topframe,text="Insert requested Hashtag for Prediction : #")
label_h.pack(side=LEFT)
textbox_h=Entry(topframe)
textbox_h.pack(side=LEFT)


#MIDDLE FRAME#
middleframe=Frame(root)
middleframe.pack()
label_ts=Label(middleframe,text="Set Duration of a Time-Series : ")
label_ts.pack(side=LEFT)
time_options={"current":0,"1 hour":1,"2 hour":2,"3 hour":3,"4 hour":4,"5 hour":5,"6 hour":6,"7 hour":7,"8 hour":8,"9 hour":9,"10 hour":10,"11 hour":11,"12 hour":12,"13 hour":13,"14 hour":14,"15 hour":15,"16 hour":16,"17 hour":17,"18 hour":18,"19 hour":19,"20 hour":20,"21 hour":21,"22 hour":22,"23 hour":23}
variable=StringVar(middleframe)
variable.set("current")
option_menu_time=OptionMenu(middleframe,variable,*time_options.keys())
option_menu_time.pack(side=RIGHT)
variable.trace("w",get_duration)


# 3RD FRAME #
middle2frame=Frame(root)
middle2frame.pack()
label_uploadfile=Label(middle2frame,text="OR Upload csv file :")
label_uploadfile.pack(side=LEFT)
button_uploadfile=Button(middle2frame,fg="red",text="Select",command=lambda: start_submit_thread("None",0,False))
button_uploadfile.pack(side=RIGHT)


#BOTTOM FRAME #
bottomframe=Frame(root)
bottomframe.pack()
run_button=Button(bottomframe,fg="blue",text="Run",command=lambda : start_submit_thread(textbox_h.get(),get_duration(),True))
run_button.pack()



def status_page():
    root2=tk.Toplevel()
    root2.title("Status ")
    root2.geometry("500x350")
    topFrame=Frame(root2)
    topFrame.pack()

    
    label_status=Label(topFrame,text="Status . . . . . . . ")
    label_status.pack()
    
    progressBar = Progressbar(topFrame, style="red.Horizontal.TProgressbar",orient="horizontal",length=350,  mode="determinate")
    progressBar.start(25)
    progressBar.pack(side=LEFT)
    
    
def result_page(text,date_time_dic):
    root3=Toplevel()
    root3.title("Results")
    root3.geometry("500x350")
    
    middleFrame=Frame(root3)
    middleFrame.pack()

    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
    from matplotlib.figure import Figure
    from matplotlib import pyplot as plt
    f=plt.figure()
    x_axis=[]
    y_axis=[]
    temp=''
    plt.ylim([-1,1])
    for key,value in date_time_dic.items():
        temp+=key+',' 
        print(key)

        for x,y in value:
            print(x,y)
            x_axis.append(x)
            y_axis.append(y)
                        
        f.suptitle('Prediction for: #'+text,fontsize=12)
        plt.plot(x_axis,y_axis,label=key,marker='o',markersize=8)
        plt.xlabel('Time',fontsize=16)
        plt.ylabel('Prediction',fontsize=16)
        x_axis=[]
        y_axis=[]
    plt.legend()

    canvas = FigureCanvasTkAgg(f, middleFrame)
    canvas.show()
    canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
    toolbar = NavigationToolbar2TkAgg(canvas, middleFrame)
    toolbar.update()
    canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)    
    
    
    

root.mainloop()
