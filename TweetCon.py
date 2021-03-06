#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 18:58:22 2018

@author: yaron
"""
from __future__ import print_function
import csv
import tweepy 
from tweepy import OAuthHandler 
import os.path
import utility as uti
import DataBase

file_path='./csvData/hashtag_tweets.csv'

class TwitterClient(object):

    
    def __init__(self,consumer_key,consumer_secret,access_token,access_token_secret):

        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
  
        except: 
            print("Error: Authentication Failed") 
        
            
    def getTweets(self,query,count=10):
         tweets = [] 
  
         try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count, lang='en',entities={}) 
            
            for tweet in fetched_tweets:
                parsed_tweet = {} 
                 # saving text of tweet 
                if( tweet.lang=="en"):
                    parsed_tweet['Tweets'] = tweet.text
                # saving time 
                parsed_tweet['Date'] = str(tweet.created_at)
              
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            # return parsed tweets 
            return tweets
        
         except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e))

    
def createCsv(inquery,tweets):
     fields_name=['Predict','Date','Tweets']
     
     file_path="./csvData/"+inquery+"/"+inquery+"_hashtag_tweets.csv"
     flag=True
     if os.path.isfile(file_path)==False:
         print("Created a file and writing to it...\n")
         save_to_file = open(file_path, 'w',encoding="utf-8")
         writer=csv.DictWriter(save_to_file,fieldnames=fields_name)
         writer.writeheader()

     else:
         print("Editing file...\n")
         flag=False
         save_to_file = open(file_path, 'a',encoding="utf-8")
         writer=csv.DictWriter(save_to_file,fieldnames=fields_name)


     for tweet in tweets:
         writer.writerow({'Predict':'none','Date':tweet['Date'], 'Tweets':str(tweet['Tweets'])})
         
     if(flag==True):
         print("Success to create "+file_path)
     else:
         print("Success to edit "+file_path)

     save_to_file.close()
     
     

                         
def runTweetCon(inquery,runtime):
    file_path=uti.create_new_folder_by_hashtag(inquery)
    consumer_key,consumer_secret,access_token,access_token_secret=DataBase.get_authentication()   
    all_tweets=[]                       
    api=TwitterClient(consumer_key,consumer_secret,access_token,access_token_secret)
    tweets = api.getTweets(query = '#'+inquery+' -filter:retweets',count =100)
    all_tweets=tweets
    
    if len(all_tweets)>0:
        createCsv(inquery,all_tweets)
    
    
    
    return len(all_tweets)
          
                     

 
