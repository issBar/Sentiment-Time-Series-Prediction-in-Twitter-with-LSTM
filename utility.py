# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog
import csv
import os

def chooseFile():
    
        root = tk.Tk()
    
        root.update()
        root.withdraw()
        if os.name=='nt':
            file_path = filedialog.askopenfilename(filetypes=(("csv file","*.csv"),))
            flag=checkCsvfile(file_path)
            if(flag==True):
                print(file_path)
                root.destroy
                return file_path
        else:
            file_path = filedialog.askopenfilename()
            flag=checkCsvfile(file_path)
            if(flag==True):
                print(file_path)
                root.destroy
                return file_path

        
    #return file_path



def checkCsvfile(filepath):
    count_header=0
    count_pred_pos=0
    count_pred_neg=0
    with open(filepath,'r') as csvfile:
       reader=csv.reader(csvfile)
       for row in reader:
           for cell in row:
               if(cell=="Predict" or cell=="Date" or cell=="Tweets"):
                   count_header+=1
               if(cell=="none"):
                   print("Predict must have :1 or -1 not none!")
                   return False
               if(cell=='1'):
                   count_pred_pos+=1
               if(cell=='-1'):
                   count_pred_neg+=1
                   
    if(count_header==3 and count_pred_neg>0 and count_pred_pos>0) :
        return True
    else:
        print("file is not match- try:filename_pred.csv")
        return False
         
        #   for cell in row:
         #      print(cell)
               #if(cell=="Predict"):
                #   print("true")
    
def create_new_folder_by_hashtag(inquery):
    file_path="./csvData/"+inquery+"/"
    
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return file_path
