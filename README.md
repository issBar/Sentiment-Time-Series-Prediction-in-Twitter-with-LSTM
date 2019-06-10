# TWITTER PREDICTION BASED ON SENTIMENT ANALYSIS

Project support Python 3.x+
Note: It is recommended to use Anaconda distribution of Python.

## Requirements 
```
Tweepy : pip install tweepy
Library for twitter API.
```
```
### Pandas : pip install pandas
Library for analyzing data from CSV files. We used Pandas for opening and updating CSV files, filtering data, data cleaning and many more.
```
```
•	Scikit-learn
Great library for data analysis, We have used to in order to implement SVC, preprocessing, feature extraction ,  cross validation and MinMaxScaler for the LSTM model.
```
```
•	NLTK
NLTK is a leading platform to work with human language data. We used NLTK in order to implement word tokenizer.
```
```
•	Keras
Time series analysis based on LSTM can capture the complexity between time steps and predicted value. There are several deep learning methods, TensorFlow, Keras, PyTorch, Theano and more.
The project was written using Keras since it provides great flexibility and functionality. Keras contains numerous implementations of commonly used neural-network building blocks such as layers, objectives, activation functions, optimizers, and a host of tools to make working with data easier. We used Keras for implementing our LSTM model.
```
```
•	Matplotlib
Plotting library for python, it provides a MATLAB-like interface and used to plot graphs. It also provides easy use with GUI toolkits like Tkinter.
```
```
•	Sqlite3
Library that is used to create local database that doesn’t require a separate server and allows accessing the database using SQL queries.
```

# Usage #

# 1. Run GUI -> Authenticate using twitter developer account. #

# 2. Insert a Hashtag that you want to predict #
Note : It is recommended to use hot topics.

# 3. Set duration for fetching tweets #
Note : The more data, the better prediction

# 4. Select Run -> #
   • Fetching Tweets 
   Produce csv : yourInput_hashtag_tweets.csv
   • Preprocessing
   Preprocessing the data
   Produce csv : preprocess_yourInput_hashtag_tweets.csv
   • NLP
   Using NLP feature extraction,countvectorizer,stop words ...
   Builds a ML using linear SVM algorithm
   Produce csv : yourInput_hashtag_tweets_pred
   
# 5. Select percentage for prediction : #
   Example : 10% Out of 24 hours will be 2.4 hours -> 2 hours prediction.
   
# 6. Select Start -> #
   • Time-Series
   Creating stationary data by smoothing trends. replacing NaN values with Moving average algorithm 
   Produce csv : predict_yourInput_hashtag_tweets.csv
   CSV contains number of positive,negative tweets. if time was NaN - cells will be empty.
   • LSTM
   Building a neural network using LSTM units.
   Produce CSV : train_predict_yourInput_hashtag_tweets
   
   NOTE :   Each Hashtag will also plot each time-series & loss plots.
   
