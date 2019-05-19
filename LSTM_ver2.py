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
from keras.layers import LSTM
import datetime
import csv
import os
import time
from matplotlib.dates import DateFormatter



def save_plot__of_predictions(input_,size_of_prediction):
    
    
    file="./csvData/"+input_+"/train_predict_"+input_+"_hashtag_tweets.csv"
    df=pd.read_csv(file)
    size_of_new_file=df.shape[0]

    
    df.set_index('Date and time')
    
    end_i_train=size_of_new_file-size_of_prediction
    

    x_time=df.index[end_i_train:]
    y_predictions=df['average'].loc[end_i_train:]
   
    
    original_file=readFile(input_)    
    df_o=pd.read_csv(original_file)
    df_o.set_index('Date and time')
    
    original_x=df_o.index[end_i_train:]
    original_y=df_o['average'].loc[end_i_train:]
    
    f=plt.figure()
    plt.ylim([-1,1])
    plt.plot(df.index,df['average'])
    plt.plot(x_time,y_predictions ,color='orange')
    plt.plot(original_x,original_y,color='red')
    f.suptitle('Next Hour Prediction',fontsize=12)
    plt.figure(figsize=(12 , 8))
    plt.title("#"+input_+" prediction graph ")#for date : +key)
    plt.gcf().autofmt_xdate(bottom=0.3, rotation=50, ha='right', which=None)
    plt.xlabel('Time-Series',fontsize=16)
    plt.ylabel('Predict',fontsize=16)
    plt.show()
 
def readFile(inquery):
    file_to_read="./csvData/"+inquery+"/predict_"+inquery+"_hashtag_tweets.csv"
    return file_to_read


def main_pred(input_):
    new_file="./csvData/"+input_+"/train_predict_"+input_+"_hashtag_tweets.csv"
    file=readFile(input_)
    df=pd.read_csv(file).set_index('Date and time')
    size_of_file=df.shape[0]

    #size of prediction time
    size_of_prediction=int(size_of_file/5)
    fields_name=['Date and time', 'count_pos','count_neg','average']
    
    array_of_data=df.iloc[:size_of_file-size_of_prediction,:]
    #saving data without predicted value
    pd.DataFrame(array_of_data).to_csv(new_file)
    
    #reading
    new_df=pd.read_csv(new_file).set_index('Date and time')
    
    new_size_of_file=new_df.shape[0]
    last_date=new_size_of_file-1
    
    

    date_and_time=df.index[last_date]
    print(date_and_time)
    date_and_time=date_and_time.split(' ')
    date=date_and_time[0].split('-')
    time=date_and_time[1].split(':')
    
    
    print('last date:',date)
    
    date=datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),0,0)
    time_pred_dic=[]
    for i in range(size_of_prediction):
        
        dt_dict,time,predicted_value=run_LSTM(input_,i+1,size_of_prediction)
        save_to_file = open(new_file, 'a',encoding="utf-8")
        writer=csv.DictWriter(save_to_file,fieldnames=fields_name)
        date+=datetime.timedelta(hours=1)
        print(' new Date and time:',date)
        writer.writerow({'Date and time':date, 'count_pos':0,'count_neg':0,'average':predicted_value[0]})
        save_to_file.close()
        
    save_plot__of_predictions(input_,size_of_prediction)

    return dt_dict,time,predicted_value

def run_LSTM(input_,round_index,size_of_prediction):
    #taking real file
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
    #scaler=MinMaxScaler(feature_range=(-1,1))
    series=pd.DataFrame(df.values)

    #Shifting the series for predicting values
    n_steps=6
    df_c=series.copy()
    for i in range(n_steps):
        series=pd.concat([series,df_c.shift(-(i+1))],axis=1)


    series.dropna(axis=0,inplace=True)

    train=series.iloc[:,:-1]
    test=series.iloc[:,n_steps:n_steps+1]

    X=list()
    Y=[]
    for i in range(len(train)):
        X.append(train.iloc[i,].values)

    for i in range(len(test)):
        Y.append(test.iloc[i,].values)

    
    X=np.array(X)   
    
    n_batch=len(X)
    # reshape from [samples, timesteps] into [samples, timesteps, features]
    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    print('x shape=',X.shape[0])
    
    model = Sequential()
    model.add(LSTM(64,activation='tanh',input_shape=(n_steps, n_features),return_sequences=False,bias_initializer='ones'))
    #model.add(LSTM(100, activation='tanh'))
    model.add(Dense(1, activation='tanh'))
    model.summary()
    model.compile(optimizer='adam', loss='mse')
    early_stop = EarlyStopping(monitor='loss', patience=2, verbose=2)
    history=model.fit(X, test, epochs=100,validation_split=0.2, shuffle=False,callbacks=[early_stop],verbose=1)


    last_batch_index=len(Y)-n_steps
    #### demonstrate prediction#####
    x_input = np.array(Y[len(Y)-n_steps:])
    print('x input=',x_input)
    
    x_input = x_input.reshape((1, n_steps, n_features))
    y_pred = model.predict(x_input, verbose=1)
    
    #df_o[size_of_o_file-1-size_of_prediction+round_index]
    print('Expected',0, 'Predicted', y_pred)
    
        
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
    
    
    f=plt.figure()
    x_axis=[]
    y_axis=[]
    #Plotting graphs by Date and Hours 
    for key,value in dt_dic.items():
        for x in value:
            x_axis.append(x[0])
            y_axis.append(x[1]) 
            
        plt.plot(x_axis,y_axis,label=key,marker='o',markersize=8)
        f.suptitle('Next Hour Prediction',fontsize=12)
        plt.figure(figsize=(12 , 8))
        plt.ylim([-1,1])
        plt.title("#"+input_+" prediction graph ")#for date : +key)
        plt.gcf().autofmt_xdate(bottom=0.3, rotation=50, ha='right', which=None)
        plt.xlabel('Time-Series',fontsize=16)
        plt.ylabel('Predict',fontsize=16)
        x_axis=[]
        y_axis=[]
        
        path='./csvData/'+input_+'/plots/'
        if not os.path.exists(path):
            os.makedirs(path)
        plt.savefig('./csvData/'+input_+'/plots/'+input_+'_plot_'+key+'.png')

    
    #Validation vs training set for viewing loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model train vs validation loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper right')
    plt.show()
    

    return dt_dic,df.index[len(df)-1],y_pred[0]
    




            
main_pred('Trump')  