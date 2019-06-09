# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 14:13:19 2019

@author: itsba
"""
import nltk
nltk.download('stopwords')

import re
import sys
#from utils import write_status
from nltk.stem.porter import PorterStemmer
#import TweetCon
import csv
from collections import OrderedDict
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


file_data_set=['./csvData/dataset.csv','./csvData/preprocess_dataset.csv']
file_divid_dataset=['./csvData/dataset.csv','./csvData/preprocess_dataset_sample.csv']
#file_tweets=['./csvData/hashtag_tweets.csv','./csvData/preprocess_hashtag_tweets.csv']

def preprocess_word(word):
    # Remove punctuation
    word = word.strip('\'"?!,.():;')
    # Convert more than 2 letter repetitions to 2 letter
    # funnnnny --> funny
    word = re.sub(r'(.)\1+', r'\1\1', word)
    # Remove - & '
    word = re.sub(r'(-|\')', '', word)
    return word


def is_valid_word(word):
    # Check if word begins with an alphabet
    return (re.search(r'^[a-zA-Z][a-z0-9A-Z\._]*$', word) is not None)


def handle_emojis(tweet):
    # Smile -- :), : ), :-), (:, ( :, (-:, :')
    tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' EMO_POS ', tweet)
    # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' EMO_POS ', tweet)
    # Love -- <3, :*
    tweet = re.sub(r'(<3|:\*)', ' EMO_POS ', tweet)
    # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' EMO_POS ', tweet)
    # Sad -- :-(, : (, :(, ):, )-:
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' EMO_NEG ', tweet)
    # Cry -- :,(, :'(, :"(
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' EMO_NEG', tweet)
    return tweet


def preprocess_tweet(tweet):
    processed_tweet = []
    # Convert to lower case
    tweet = tweet.lower()
    # Replaces URLs with the word URL
    tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', ' URL ', tweet)
    # Replace @handle with the word USER_MENTION
    tweet = re.sub(r'@[\S]+', 'USER_MENTION', tweet)
    # Replaces #hashtag with hashtag
    tweet = re.sub(r'#(\S+)', "HASHTAG", tweet)
    # Remove RT (retweet)
    tweet = re.sub(r'\brt\b', '', tweet)
    # Replace 2+ dots with space
    tweet = re.sub(r'\.{2,}', ' ', tweet)
    # Strip space, " and ' from tweet
    tweet = tweet.strip(' "\'')
    # Replace emojis with either EMO_POS or EMO_NEG
    tweet = handle_emojis(tweet)
    # Replace multiple spaces with a single space
    tweet = re.sub(r'\s+', ' ', tweet)
   
    words = tweet.split()
    tweet=word_tokenize(tweet)
    
    ps = PorterStemmer()
    words = [ps.stem(word) for word in words if not word in set(stopwords.words('english'))]

    for word in words:
        word = preprocess_word(word)
        if is_valid_word(word):
            processed_tweet.append(word)

    return ' '.join(processed_tweet)


def preprocess_dataset(csv_file_name,csv_file_name_p):
    try:
        df=pd.read_csv(csv_file_name,header=None,usecols=[0,2,5], names=['Predict','Date','Tweets'],encoding="iso-8859-1")
        size=df.shape[0]
        with open(csv_file_name_p, 'w',encoding="utf-8") as csvfile:
            fieldnames=['Predict','Date','Tweets']
            writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
            writer.writeheader()
            for i in range(size):
                processed_tweet=preprocess_tweet(str(df['Tweets'][i]))
                writer.writerow({'Predict':str(df['Predict'][i]),'Date':str(df['Date'][i]),'Tweets':processed_tweet})
    except FileNotFoundError:        
        print("Error in file")
        exit
        

    print ('\nSaved processed tweets to: %s' % csv_file_name_p)
    
    

def preprocess_Tweets(csv_file_name, processed_file_name):
    save_to_file = open(processed_file_name, 'w',encoding="utf-8")
    fields_name=['Predict','Date','Tweets']
    writer=csv.DictWriter(save_to_file,fieldnames=fields_name)
    writer.writeheader()
    try:
        with open(csv_file_name, 'r',encoding="utf-8") as csvt:
            reader=csv.DictReader(csvt)
            for row in reader:
                processed_tweet = preprocess_tweet(row['Tweets'])
                writer.writerow({'Predict':'none','Date':row['Date'] , 'Tweets':processed_tweet })
        save_to_file.close()
        print ('\nSaved processed tweets to: %s' % processed_file_name)
        return processed_file_name
    except FileNotFoundError:  
        print("Error in file")
        exit


    
def divide_dataset(csv_file_name,preprocessed_dataset_sample):
    df=pd.read_csv(csv_file_name,header=None,usecols=[0,2,5], names=['Predict','Date','Tweets'],encoding="iso-8859-1")
    count_neg=800000
    try:
        with open(preprocessed_dataset_sample, 'w',encoding="utf-8") as csvfile:
            fieldnames=['Predict','Date','Tweets']
            writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
            writer.writeheader()
            for i in range(800000):
                processed_tweet=preprocess_tweet(str(df['Tweets'][i]))
                if(str(df['Predict'][i])=='0'):
                    writer.writerow({'Predict':'1','Date':str(df['Date'][i]),'Tweets':processed_tweet})
            for i in range(count_neg,count_neg+800000):
                
                processed_tweet=preprocess_tweet(str(df['Tweets'][i]))
                if(str(df['Predict'][i])=='4'):
                    writer.writerow({'Predict':'-1','Date':str(df['Date'][i]),'Tweets':processed_tweet})
    
        print ('\nSaved  divid processed tweets to: %s' % preprocessed_dataset_sample)
    except FileNotFoundError:  
        print("Error in file")
        exit


def run_preprocess_dataset():
    print('start function preprocess_dataset\n')
    preprocess_dataset(file_data_set[0],file_data_set[1])
    
def run_preprocess_Tweets(inquery):
    
    if inquery!=' ':
        file_tweets=["./csvData/"+inquery+"/"+inquery+"_hashtag_tweets.csv","./csvData/"+inquery+"/preprocess_"+inquery+"_hashtag_tweets.csv"]
        print('Starts function preprocess_Tweets\n')
        preprocess_Tweets(file_tweets[0],file_tweets[1])
        print("Successed preprocessing tweets")
    else:
        print("No such directory")
        

def run_divide_dataset():
    print('start function divide_dataset\n')
    divide_dataset(file_divid_dataset[0],file_divid_dataset[1])

def runPreprocess(inp,inquery):
    switcher={1:run_preprocess_dataset,
              2:run_preprocess_Tweets(inquery),
              3:run_divide_dataset}
        
    func=switcher.get(inp,lambda:'invaild function\n')


#runPreprocess(3,' ')
#runPreprocess(2,"gameofthrones") 
#runPreprocess(2,"ml")