# Natural Language Processing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import sys

# Cleaning the texts
import re
import nltk

from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.svm import SVC 
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from nltk.corpus import sentiwordnet as swn
from sklearn.feature_extraction.text import CountVectorizer



#create a vocabulary of the dataset
def build_voc(Range,datasets):
    all_words=[]
    for i in range(Range):
        all_words.extend(datasets['Tweets'][i])
    wordlist=nltk.FreqDist(all_words)
    word_features=wordlist.keys()
    
    return word_features
    
def extract_features(word_features,tweet):
    tweet_words=set(tweet)
    features={}
    for word in word_features:
        features['contains(%s)'%word]=(word in tweet_words)
    return features


def getCorpus(Range,datasets):
    corpus = []
    for i in range(Range):
        review = str(datasets['Tweets'][i])
        review = review.split()
        review = ' '.join(review)
        corpus.append(review)
        
    return corpus


def dataset_count_vectorizer(dataset,corpus,tweets_data_size):
    print('starting dataset_count_vectorizer')
    vectorizer=CountVectorizer(max_df=1.0)
    X=vectorizer.fit_transform(corpus).toarray()
    y = dataset.iloc[:, 0].values
    voc=vectorizer.get_feature_names()
    
    return X,y,voc,vectorizer


def senti_word_analysis(voc,X):
    swn_weights=[]
    print("",voc)
    for word in voc:
        try:
            # Put this code in a try block as all the words may not be there in sentiwordnet (esp. Proper
            # nouns). Look for the synsets of that word in sentiwordnet 
            print(word)

            synset=list(swn.senti_synsets(word))
            print("ghjghjgjhjjj")

            # use the first synset only to compute the score, as this represents the most common 
            # usage of that word 
            common_meaning =synset[0]
            # If the pos_Score is greater, use that as the weight, if neg_score is greater, use -neg_score
            # as the weight 
            if common_meaning.pos_score()>common_meaning.neg_score():
                weight=common_meaning.pos_score()
            elif common_meaning.pos_score()<common_meaning.neg_score():
                weight=-common_meaning.neg_score()
            else: 
                weight=0
        except : 
            weight=0
            e = sys.exc_info()[0]
            print(e)

        swn_weights.append(weight)
        
    swn_X=[]
    for row in X: 
        swn_X.append(row.dot(np.array(swn_weights)))
        # Convert the list to a numpy array 
    
    print("",swn_weights)

    swn_X=np.vstack(swn_X)
    return swn_X,swn_weights



def getBagOfWords_dataset(corpus,dataset):
    cv = CountVectorizer(max_features = 178)
    X = cv.fit_transform(corpus).toarray()
    y = dataset.iloc[:, 0].values
    
    return X,y


def getBagOfWords_tweet(corpus,tweets_data):
    cv = CountVectorizer(min_df=1)
    z = cv.fit_transform(corpus).toarray()
    t = tweets_data.iloc[:, 0].values
    
    return corpus,t


def save_PredToCsv(pred,Range,tweets_data,inquery):
    index=0
   # dataset = pd.read_csv('./csvData/preprocess_hashtag_tweets.csv')
        
    with open("./csvData/"+inquery+"_hashtag_tweets_pred.csv", 'w',encoding="utf-8") as csvfile:
        fieldnames=['Predict','Date','Tweets']
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        for i  in range(Range):
            writer.writerow({'Predict':pred[index],'Date':tweets_data['Date'][i],'Tweets':tweets_data['Tweets'][i]})
            index+=1
        print ('\nSaved prediction for tweets to: preprocess_'+inquery+'_hashtag_tweets_pred.csv\n')



def get_Score(model,X_train, X_test, y_train, y_test,X_tweet,y_tweet):
    model.fit(X_train,y_train)
    y_pred=model.predict(X_tweet)

    return model.score(X_test,y_test),y_pred


def ml(X,y,X_tweet,y_tweet,tweets_data_size,tweets_data,inquery):
    
    score_svm=[]
    X=np.array(X)
    #svc=LinearSVC()
    kf=StratifiedKFold(n_splits=10,shuffle=True,random_state=None)
    for train,test in kf.split(X,y):
            X_train = X[train]
            X_test = X[test]
            y_train = y[train]
            y_test = y[test]
      
        
           # tf_transformer=TfidfTransformer(use_idf=False).fit(X_train)
            #X_train_tf=tf_transformer.transform(X_train)
            #X_test_idf=tf_transformer.transform(X_test)
            vectorizer=CountVectorizer()
            X_train=vectorizer.fit_transform(X_train)
            voc=vectorizer.get_feature_names()
            swn_X,swn_weights=senti_word_analysis(voc,X_train)
            y_train=np.array(y_train)
            svm_ml(swn_X,y_train,vectorizer,X_tweet,swn_weights)
            #score_svc,y_pred_svc=get_Score(LinearSVC(),X_train,X_test,y_train,y_test,X_tweet,y_tweet)
            #score_svm.append(score_svc)
           

           # svc.fit(X_train,y_train)
           #y_pred_tweet=svc.predict(X_tweet)           
    #save_PredToCsv(y_pred_svc,tweets_data_size,tweets_data,inquery)


    print("SVM= ",score_svm)    
    
def svm_ml(swn_X,y,vectorizer,tweets,swn_weights):
    print( "starting svm ml..\n")
    vec=CountVectorizer()
    
    SVMClassifier=SVC()
    SVMClassifier.fit(swn_X,y)
    print("Im here")
    #print("SVM score=",SVMClassifier.score())
    SVMResultLabels=[]
    for tweet in tweets:
        tweet_sentence=''
        for word in tweet:
            tweet_sentence=' '.join(word)
            svmFeatures=vec.fit_transform([tweet_sentence]).toarray().dot(np.array(swn_weights))
            SVMResultLabels.append(SVMClassifier.predict(svmFeatures)[0])
        
    print("SVM Results : ",SVMResultLabels)

    return SVMResultLabels

def run_natural_language_processing(inquery):
    print("starting function run_natural_language_processing\n")
    # Importing the dataset
    dataset = pd.read_csv('./csvData/preprocess_dataset_sample.csv')
    tweets_data= pd.read_csv('./csvData/preprocess_'+inquery+'_hashtag_tweets.csv')

    dataset_size=dataset.shape[0]
    tweets_data_size=tweets_data.shape[0]
    
        
    #word_features=build_voc(dataset)
    #trainingFeatures=nltk.classify.apply_features(extract_features,dataset)
    corpusDataset=getCorpus(dataset_size,dataset)
    #X,y=getBagOfWords_dataset(corpusDataset,dataset)
    #X,y,voc,vectorizer=dataset_count_vectorizer(dataset,corpusDataset,tweets_data_size)
    #swn_X,swn_weights=senti_word_analysis(voc,X)
    y = dataset.iloc[:, 0].values

    corpusTweets=getCorpus(tweets_data_size,tweets_data)
    #svm_ml(swn_X,y,vectorizer,corpusTweets,swn_weights)
    X_tweet,y_tweet=getBagOfWords_tweet(corpusTweets,tweets_data)

    ml(corpusDataset,y,X_tweet,y_tweet,tweets_data_size,tweets_data,inquery)


