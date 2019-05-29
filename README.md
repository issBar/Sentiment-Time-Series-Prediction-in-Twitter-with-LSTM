# FP
Prediction on twitter based on sentiment analysis

Project support Python 3.x+
It is recommended to run on Anaconda using spyder
______________________
# RUN PROGRAM USING GUI #
1. Run GUI -> Login with your personal Twitter developer account
2. Type in a requested hashtag and set requested fetch time.

_________________
 # IF YOU WANT TO RUN SEPERATELY WITHOUT A GUI #
 
1. Run TweetCon.py and insert hashtag input and time
2. Preprocess.py -> It will deploy a new csv file after preprocessing
3. NLP.py -> It will deploy a new csv file after performing Sentiment analysis & Natural language processing concepts on a Machine learning (SVM) which trains over 1.6million tweets (Sentiment140).
              Produce a classified (1:POSITIVE , -1:NEGATIVE) csv file.
4.TimeSeries.py -> builds a time-series csv file and uses polarity over 1 hour of data.
5.LSTM.py -> This will generate a csv file of predicted values of 20% of the real data. plots of all the data by dates
