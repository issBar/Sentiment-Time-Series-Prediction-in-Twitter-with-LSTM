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


def readFile(inquery):
    file_to_read="./csvData/"+inquery+"/predict_"+inquery+"_hashtag_tweets.csv"
    return file_to_read

def run_LSTM(input_):
    # fix random seed for reproducibility
    np.random.seed(7)

    #taking csv file   
    file=readFile(input_)
    df=pd.read_csv(file).set_index('Date and time')
    df.drop(['count_pos','count_neg'],axis=1,inplace=True)
    df = df.sort_values(['Date and time'])
    size_of_file=df.shape[0]

    #Column we want to predict
    target_name=['average']

    #MinMax Scaler
    scaler=MinMaxScaler(feature_range=(-1,1))
    #scaled=scaler.fit_transform(df.values)
    series=pd.DataFrame(df.values)

    #Shifting the series for predicting values
    n_steps=3
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
 
    # reshape from [samples, timesteps] into [samples, timesteps, features]
    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))

    model = Sequential()
    model.add(LSTM(100,activation='tanh',input_shape=(n_steps, n_features),return_sequences=False))
    #model.add(LSTM(100, activation='tanh'))
    model.add(Dense(1, activation='tanh'))
    model.summary()
    model.compile(optimizer='adam', loss='mse')
    early_stop = EarlyStopping(monitor='loss', patience=2, verbose=2)
    history=model.fit(X, test, epochs=100,validation_split=0.45, shuffle=False,callbacks=[early_stop],verbose=1)


    last_batch_index=len(Y)-n_steps
    # demonstrate prediction
    x_input = np.array(Y[len(Y)-n_steps-1:-1])
    x_input = x_input.reshape((1, n_steps, n_features))
    y_pred = model.predict(x_input, verbose=1)



    print('Expected', Y[len(Y)-1], 'Predicted', y_pred)
    
        
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
     
        f.suptitle('Next Hour Prediction',fontsize=12)
        plt.figure(figsize=(10 , 6))
        plt.ylim([-1,1])
        plt.title("#"+input_+" prediction graph for date : "+key)
        plt.plot(x_axis,y_axis,label=key,marker='o',markersize=8)
        plt.gcf().autofmt_xdate(bottom=0.3, rotation=50, ha='right', which=None)
        plt.xlabel('Time-Series',fontsize=16)
        plt.ylabel('Predict',fontsize=16)
        x_axis=[]
        y_axis=[]
        plt.savefig('./csvData/'+input_+'/'+input_+'_plot'+key+'.png')


    #Plotting predicted value
    split_date=df.index[len(df)-1].split(' ')
    plt.plot(split_date[1],y_pred[0] ,marker='s')
    plt.savefig('./csvData/'+input_+'/'+input_+'_plot_prediction.png')
    plt.show()
    
    #Validation vs training set for viewing loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model train vs validation loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper right')
    plt.show()
    
    return dt_dic,df.index[len(df)-1],y_pred[0]
    
            
#run_LSTM('Trump')  