#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 17:19:12 2019

@author: bar
"""
import pandas as pd
import csv
import datetime
import utility as uti


    
def handling_missing_values(inquery):
    #Filling in missing hours of time-series and setting default value as average of both previous and next value
    #This function is needed in-order to create a correct time-series dependencies
    file_to_read="./csvData/"+inquery+"/predict_"+inquery+"_hashtag_tweets.csv"
    df=pd.read_csv(file_to_read)
    size_of_file=df.shape[0]
    df['Date and time']=pd.to_datetime(df['Date and time']) #convert to date time
    df.index=pd.to_datetime(df.index) #convert to date and time
    df=df.set_index('Date and time').resample('H').mean().fillna((df['average'].fillna(method='ffill')+df['average'].fillna(method='bfill'))/2)
    df['average']=df['average'].where(df['average'].notnull(), other=(df['average'].fillna(method='ffill')+df['average'].fillna(method='bfill'))/2)
    array_of_data=df.iloc[:]
    print(array_of_data)
    pd.DataFrame(array_of_data).to_csv(file_to_read)

    
    
    
def create_pred_file(date_time_dic,inquery):
    with open("./csvData/"+inquery+"/predict_"+inquery+"_hashtag_tweets.csv", 'w',encoding="utf-8") as csvfile:
        fieldnames=['Date and time','count_pos','count_neg','average']
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        for key,value  in date_time_dic.items():
            for hour,count_pos,count_neg,avg in value:  
                    temp=min_date_to_min_dt(key,hour)
                    writer.writerow({'Date and time':temp,'count_pos':count_pos,'count_neg':count_neg,'average':avg})
          
        print ('\nSaved prediction for tweets to: predict_'+inquery+'_hashtag_tweets.csv\n')
        


def min_date_to_min_dt(min_date,min_hour):
    min_date=str(min_date)
    sp=min_date.split('/')
    date_and_time=datetime.datetime(int(sp[2]),int(sp[1]),int(sp[0]),int(min_hour),0,0)
    return date_and_time


def run_time_series(inquery,flag):
    
    #check if inquery is from user input
    if(flag==True):
        file_to_read="./csvData/"+inquery+"/"+inquery+"_hashtag_tweets_pred.csv"
    else:
        file_to_read=uti.chooseFile()
        print(file_to_read)
        
    #reading from file 
    df=pd.read_csv(file_to_read).set_index('Date')
    df.index=pd.to_datetime(df.index) #convert to date time
    df = df.sort_values(["Date"])
    #sets as a series of values
    ts=pd.Series(df.loc[:,'Predict'].values,index=df.index,name="tweet pred",)


    #spliting data from csv and save them to lists
    avglist=[]
    date=[]
    time=[]
    hours=[]
    minutes=[]
    prediction=[]
    date_and_time=[]
    sum_pos=0
    sum_neg=0
    size=df.shape[0]
    date_time_dic={}

    for row in reversed(range(size)): #Splitting data from csv
   
        date.append(df.index[row].strftime('%d/%m/%Y'))
        time.append(df.index[row].strftime('%H:%M:%S'))
        date_and_time.append(df.index[row].strftime('%Y/%m/%d %H:%M:%S'))
        hours.append(df.index[row].strftime('%H'))
        minutes.append(df.index[row].strftime('%M'))
        prediction.append(df['Predict'][row])
        
   #intilaize data to plot
    count=0
    count_by_hour=0    
    max_time=hours[0]
    min_time=hours[size-1]
    
    min_date=date[size-1]
    max_date=date[0]
   
    
    for row in reversed(range(size)):
        count=count+1

        #creates a avg list which calculates the average of current hour tweets
        if hours[row]!=min_time :
                avglist.append((int(min_time),sum_pos,sum_neg,(((sum_pos)-(sum_neg))/count_by_hour)))
                count_by_hour=0
                sum_neg=0
                sum_pos=0
                min_time=hours[row]
                    
        
        if count<=size:
            count_by_hour=count_by_hour+1
            if(prediction[row]==1):
                sum_pos=sum_pos+1
            elif(prediction[row]==-1):
                sum_neg=sum_neg+1
                
        if(min_time==max_time and count==size and count_by_hour>0):
                avglist.append((int(min_time),sum_pos,sum_neg,(((sum_pos)-(sum_neg))/count_by_hour)))
        
        if date[row]!=min_date: #different date      
            date_time_dic[min_date]=avglist #Dictionary : {'Date':[Hour,Avg prediction of current hour]}
            avglist=[] #clearing list
            min_date=date[row] #setting new date value
          
           
        if date[row]==max_date:
            date_time_dic[max_date]=avglist
        

    #save to  csv file 
    create_pred_file(date_time_dic,inquery)
    
    handling_missing_values(inquery)
  


run_time_series("gameofthrones",True)