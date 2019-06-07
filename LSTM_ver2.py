# -*- coding: utf-8 -*-
"""
Created on Sun May  5 22:37:42 2019

@author: itsba
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping
from keras.layers import Dropout
from keras.layers import LSTM
import datetime
import csv
import os
import time
from matplotlib.dates import DateFormatter
import pylab as pl
import matplotlib.dates as mdates

def save_plot__of_predictions(input_,size_of_prediction):
    
    #reading from prediction file
    file="./csvData/"+input_+"/train_predict_"+input_+"_hashtag_tweets.csv"
    df=pd.read_csv(file)
    size_of_new_file=df.shape[0]
    df.set_index('Date and time')
    #index of last data point we train
    end_i_train=size_of_new_file-size_of_prediction

    x_time=df.index[end_i_train:]
    y_predictions=df['average'].loc[end_i_train:]

    
    original_file=readFile(input_)    
    df_o=pd.read_csv(original_file)
    df_o.set_index('Date and time')
    
    original_x=df_o.index[end_i_train:]
    original_y=df_o['average'].loc[end_i_train:]
    
    print("Real Value : ",original_y, "Predicted Value : ",y_predictions)
    
    f=plt.figure()
    plt.figure(figsize=(6 ,4))
    plt.ylim([-1,1])
    plt.plot(df.index,df['average'])
    plt.plot(original_x,original_y,color='blue',marker='o')
    plt.plot(x_time,y_predictions ,color='orange',marker='o')
    
    plt.suptitle('Prediction graph for #'+input_,fontsize=12)
                 
    try:
            
        path_loss='./csvData/'+input_+'/plots/'
        if not os.path.exists(path_loss):
            os.makedirs(path_loss)
        plt.savefig('./csvData/'+input_+'/plots/'+input_+'_prediction_plot.png')
    except FileNotFoundError:
        print('file not exist!\n')
            
            
    '''
    plt.title("#"+input_+" prediction graph ")#for date : +key)
    plt.gcf().autofmt_xdate(bottom=0.3, rotation=50, ha='right', which=None)
    plt.xlabel('Time-Series',fontsize=16)
    plt.ylabel('Predict',fontsize=16)
    plt.show()
    '''
def readFile(inquery):
    file_to_read="./csvData/"+inquery+"/predict_"+inquery+"_hashtag_tweets.csv"
    return file_to_read


def main_pred(input_,percentage):
    new_file="./csvData/"+input_+"/train_predict_"+input_+"_hashtag_tweets.csv"
    file=readFile(input_)
    df=pd.read_csv(file).set_index('Date and time')
    size_of_file=df.shape[0]+1
    
    #size of prediction time - (forward)
    size_of_prediction=int(size_of_file*percentage)
    fields_name=['Date and time', 'count_pos','count_neg','average']
    
    array_of_data=df.iloc[:size_of_file-size_of_prediction,:]
    #saving data without predicted value
    pd.DataFrame(array_of_data).to_csv(new_file)
    
    #reading
    new_df=pd.read_csv(new_file).set_index('Date and time')
    new_size_of_file=new_df.shape[0]
    last_date=new_size_of_file-1
    print(df.index[last_date])
    #Splitting date and time
    date_and_time=df.index[last_date]
    date_and_time=date_and_time.split(' ')
    date=date_and_time[0].split('-')
    time_=date_and_time[1].split(':')
    print('last date:',date)
    
    #set o' clocks
    dt_dict={}
    date=datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time_[0]),0,0)
    time_pred_dic=[]
    predicted_value=[]
    for i in range(size_of_prediction):
        
        dt_dict,predicted_value=run_LSTM(input_,i+1,size_of_prediction)
        
        save_to_file = open(new_file, 'a',encoding="utf-8")
        writer=csv.DictWriter(save_to_file,fieldnames=fields_name)
        date+=datetime.timedelta(hours=1)
        print(' new Date and time:',date)
        writer.writerow({'Date and time':date, 'count_pos':0,'count_neg':0,'average':predicted_value[0]})
        save_to_file.close()
        time.sleep(2)
    #saving plots    
    save_plot__of_predictions(input_,size_of_prediction)
    
    print("dt_dict==",dt_dict)
    return dt_dict,predicted_value,size_of_prediction

def run_LSTM(input_,round_index,size_of_prediction):
    #taking real file
    print("run_lstm\n")
    real_file=readFile(input_)
    df_o=pd.read_csv(real_file)
    size_of_o_file=df_o.shape[0]
    
    #taking csv file   
    file="./csvData/"+input_+"/train_predict_"+input_+"_hashtag_tweets.csv"
    df=pd.read_csv(file).set_index('Date and time')
    df.drop(['count_pos','count_neg'],axis=1,inplace=True)
    df = df.sort_values(['Date and time'])
    size_of_file=df.shape[0]
    
    #Column we want to predict
    target_name=['average']

    #MinMax Scaler
    scaler=MinMaxScaler(feature_range=(-1,1))
    #series=scaler.fit_transform(df.values)
    series=pd.DataFrame(df.values)

    #Shifting the series for predicting values
    n_steps=6
    df_c=series.copy()
    for i in range(n_steps):
        series=pd.concat([series,df_c.shift(-(i+1))],axis=1)


    series.dropna(axis=0,inplace=True)


    #Train and test lists
    train=series.iloc[:,:-1]
    test=series.iloc[:,n_steps:n_steps+1]

    X=list()
    Y=[]
    for i in range(len(train)):
        X.append(train.iloc[i,].values)

    for i in range(len(test)):
        Y.append(test.iloc[i,].values)


    #X=np.array(X)   
    X=scaler.fit_transform(X)
    test=scaler.fit_transform(test)

    n_batch=len(X)
    # reshape from [samples, timesteps] into [samples, timesteps, features]
    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    print('x shape=',X.shape[0])
    model = Sequential()
    model.add(LSTM(48,activation='tanh',input_shape=(n_steps, n_features),return_sequences=True,bias_initializer='ones'))
    model.add(LSTM(16, activation='tanh',return_sequences=False))
   # model.add(LSTM(16, activation='tanh'))
    model.add(Dense(1))
    model.summary()
    model.compile(optimizer='adam', loss='mse')
    early_stop = EarlyStopping(monitor='loss', patience=2, verbose=2)
    history=model.fit(X, test, epochs=100,validation_split=0.2, shuffle=False,callbacks=[early_stop],verbose=1)


    last_batch_index=len(Y)-n_steps
    #### demonstrate prediction#####
    x_input = np.array(Y[len(Y)-n_steps:])
    print('x input=',x_input)
    
    #predicition
    x_input = x_input.reshape((1, n_steps, n_features))
    y_pred = model.predict(x_input, verbose=1)
    
    y_pred=scaler.inverse_transform(y_pred)
        
    #Splitting date and hours to view on graph
    times=[]
    dates=[]
    hours=[]
    pred=[]
    for row in range(len(df)): #Splitting data from csv
        times.append(df.index[row].split(' '))
        pred.append(df['average'][row])
    
    for row in range(len(times)):
        dates.append(times[row][0])
        hours.append(times[row][1])
        
        
    min_date=dates[0]
    max_date=dates[len(dates)-1]
    dt_dic={}
    hours_list=[]
    for i in range(len(dates)):
        
        if min_date!=dates[i]:
            dt_dic[min_date]=hours_list
            min_date=dates[i]
            hours_list=[]
        if max_date==dates[i]:
            dt_dic[min_date]=hours_list
             
        hours_list.append([hours[i],pred[i]])
        
    x_axis=[]
    y_axis=[]
    #Plotting graphs by Date and Hours 
    for key,value in dt_dic.items():
        f=plt.figure()
        for x in value: 
        
            hour=x[0].split(":")
            temp=hour[0]
            x_axis.append(temp)
            y_axis.append(x[1]) 

    
        ax=plt.figure(figsize=(6 , 4))
        plt.ylim([-1,1])
        plt.xlabel('Time-Series (hours)',fontsize=10)
        plt.ylabel('Predict',fontsize=10)
        plt.title("#"+input_+" prediction graph - "+key)
        plt.plot(x_axis,y_axis,label=key,marker='o',markersize=4)
        x_axis=[]
        y_axis=[]
        
        path='./csvData/'+input_+'/plots/'
        if not os.path.exists(path):
            os.makedirs(path)
        plt.savefig('./csvData/'+input_+'/plots/'+input_+'_plot_'+key+'.png')
        plt.show()




    #Validation vs training set for viewing loss
    plt.ylim([0,4])
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model train vs validation loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper right')
    
    try:
            
        path_loss='./csvData/'+input_+'/plots/'
        if not os.path.exists(path_loss):
            os.makedirs(path_loss)
        plt.savefig('./csvData/'+input_+'/plots/'+input_+'_loss_plot_'+str(round_index)+'.png')
        print("loss fig saved\n")
        plt.show()
    except FileNotFoundError:
        print('file not exist!\n')
    #print(dt_dic)
    return dt_dic,y_pred[0]
   
    
#main_pred('Trump',0.2)
#main_pred('gameofthrones')  
#main_pred('iphone',0.1)