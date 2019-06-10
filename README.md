# TWITTER PREDICTION BASED ON SENTIMENT ANALYSIS

Project support Python 3.x+
Note: It is recommended to use Anaconda distribution of Python.

# Usage #
_____________________
1. Run GUI -> Authenticate using twitter developer account.
_________________
2. Insert a Hashtag that you want to predict 
Note : It is recommended to use hot topics.
_________________
3. Set duration for fetching tweets
Note : The more data, the better prediction
_________________
4. Select Run -> 
   # Fetching Tweets #
   Produce csv : yourInput_hashtag_tweets.csv
   # Preprocessing# 
   Preprocessing the data
   Produce csv : preprocess_yourInput_hashtag_tweets.csv
   # NLP #
   Using NLP feature extraction,countvectorizer,stop words ...
   Builds a ML using linear SVM algorithm
   Produce csv : yourInput_hashtag_tweets_pred
_________________
   
5. Select percentage for prediction : 
   Example : 10% Out of 24 hours will be 2.4 hours -> 2 hours prediction.
_________________
6. Select Start ->
   # Time-Series #
   Creating stationary data by smoothing trends. replacing NaN values with Moving average algorithm 
   Produce csv : predict_yourInput_hashtag_tweets.csv
   CSV contains number of positive,negative tweets. if time was NaN - cells will be empty.
   # LSTM #
   Building a neural network using LSTM units.
   Produce CSV : train_predict_yourInput_hashtag_tweets
   # NOTE #
   Each Hashtag will deploy Plots of time-series & loss plots.
   
