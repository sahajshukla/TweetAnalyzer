# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 21:27:23 2020

@author: Sahaj
We are using the api system with twitter client python library tweepy
We dont want to scrape the data and violate any rules and regulations because we really want to be on the white side.
The code has been greatly influenced because I myself could never use all the tweepy tools. 
"""

# Let us start by adding the credentials. I dont know if it is the best way to start but let's do it anyway
# the parameters mentioned below can be avalilable to you after ypu create your twitter developer accound and request for an api
access_token = ''
access_token_secret = ''
api_key = ''
api_key_secret = '' 

from tweepy import OAuthHandler
from tweepy import StreamListener
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import numpy as np
import pandas as pd
from textblob import TextBlob
import re

#import matplotlib.pyplot as plt

class TwitterClient(): # this whole class is used to scrape the data for just one user. Any user in specific. 
    #if we do not decide on the user, itll take our own tweets. In this case, it is my account so you better put in a user
    
    def __init__(self, twitter_user=None):
        self.auth = authentication().authenticator()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
        
    def timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    
     # I cannot emphasize on how powerful this API is. I will make quick functions that are not relevant to this project
     # At this point of time. However, they may be useful subsequently if the plan changes. One can anytime make the objects and call these functions
    def friend_names(self, num_friends):
         # this will return the list of friends 
        friends = []
        for name in Cursor(self.twitter_client.friends, id = self.twitter_user).items(num_friends):
            friends.append(name)
        return friends
    def follower_names(self, num_followers):
        # this will return a list of followers the user has
        followers = []
        for name in Cursor(self.twitter_client.followers, id = self.twitter_user).items(num_followers):
            followers.append(name)
        return followers
    def home_timeline_tweets(self, num_tweets):# this will return the n tweets one has tweeted on his timeline. 
         #NEVER USE THIS FUNCTION BECAUSE IT"S MY EFFING ID
        tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id = self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    def tweets_by_hashtag(self,num_tweets):
        tweets_here = []
        for tweet in Cursor(self.twitter_client.search,q=self.twitter_user).items(num_tweets):
            tweets_here.append(tweet)
        return tweets_here
        
        
class authentication(): # this class has been created because we want to avoid overusage of the same code and increase the lines
    # an extra module always helps to put the code in place. Just good coding practice :)
    def authenticator(self):
        auth = OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth



class TwitterStreamer():
    # this is the actual 'meat' of the code. The Listener class is referenced here and the arguments will be passed to this class
    
    def __init__(self):
        self.authentic = authentication()
        
    def stream_tweets(self):
        listener = Listener()
        auth = self.authentic.authenticator()
        stream = Stream(auth, listener)
        stream.filter(track = list_of_tweets)


class Listener(StreamListener):
    def __init__(self, filename):
        self.filename = filename
        def on_data(self, data): #this is an inbuilt method trhat we are overriding. This comes from StreamListener parent class 
            try:
                with open (self.filename, 'a') as file:
                    file.write(data)
                    return True
            except BaseException as e:
                print("There has been an error in the data method of class Listener %s:" %str(e))
                return True
            
        def on_error(self, status):
            if status == 420: # always wondered if this is used as an int or a string. Turns out, int!
                #none the less, I love this number. Jk, this is a special condition that prevents the user from getting more tweets
                # the user may also be locked out. as a joke, I'd rather be locked out than in. Quarantine sucks
                return False
            print(status)
            
class TweetToDf():
    def clean_tweet(self,this):
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", this).split())
        
    def analyse_emotion(self, tweets):
        
        analysis= TextBlob(self.clean_tweet(tweets))
        if analysis.sentiment.polarity>0:
            return 1
        elif analysis.sentiment.polarity==0:
            return 0
        else:
            return -1
        
        
    def analytics(self, tweets):
        
        df = pd.DataFrame(data = [tweet.text for tweet in tweets], columns = ['Tweets'])
        df['retweet_count'] = np.array([tweet.retweet_count for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        return df
      

#filename = 'Tweets.json' # since the data will be received in json format
#list_of_tweets = ['market', 'consumers', 'trending', 'shops', 'inflation'] 
#I am passing this random list of tweet searches but one can feel free to change the list anytime they want
client_name = []
hashtag_string = []
print_name = []
print("enter the word stop to stop entering the list ")
while True:
  temp = str(input("enter the input account from which you intend to receive the tweet  "))
  if temp == 'stop':
        break
  else:
        client_name.append(temp)
        print_name=temp
print("enter the word stop to stop entering the list ")
while True:
    temporary = str(input("enter the input hashtag to find grab the data "))
    if temporary == 'stop':
        break
    else:
        hashtag_string.append(temporary)
#client_name = str(input("enter the clients name:"))
num_tweets = int(input("enter integer input of the number of tweets you want in the dataframe. \n The number will be for each distinct hashtag:"))
final_tweets = []
final_tweets_2 = []
for each in client_name:
    client = TwitterClient(each)
    tweets = client.timeline_tweets(num_tweets)
    dataframe_object = TweetToDf()
    df = dataframe_object.analytics(tweets)# by this part, we have successfully generated a dataframe.
    df['sentiment'] = np.array([dataframe_object.analyse_emotion(tweet) for tweet in df['Tweets']])
    # this dataframe can be accessed by a separate code if stored in CSV or equivalent format
    #twitter = TwitterStreamer()
    #twitter.stream(filename, list_of_tweets)
    time_retweets = pd.Series(data = df.iloc[:,1].values, index = df.iloc[:,2])
    time_retweets.plot(figsize = (16,4), color = 'blue', label = "retweets", legend = True)
    final_tweets.append(df)
    time_likes = pd.Series(data = df.iloc[:,3].values, index = df.iloc[:,2])
    time_likes.plot(figsize = (16,4), color = 'red', label = "likes", legend = True)
    summer = 0    
    for i in df['sentiment']:
        summer+=i
    if summer>=num_tweets/5:
        print("the overall sentiment about %s is positive" %print_name)
    
    elif summer==num_tweets/5:
        print("the overall sentiment about %s is neutral" %print_name)
    else:
        print("the overall sentiment about %s is negative" %print_name)
    

for i in hashtag_string:
    client = TwitterClient(i)
    tweets_2 = client.tweets_by_hashtag(num_tweets)
    df_object = TweetToDf()
    dataframe = df_object.analytics(tweets_2)
    dataframe['sentiment'] = np.array([df_object.analyse_emotion(tweet) for tweet in dataframe['Tweets']])
    time_retweets_2 = pd.Series(data = dataframe.iloc[:,1].values, index = dataframe.iloc[:,2])
    time_retweets_2.plot(figsize = (16,4), color = 'blue', label = "retweets", legend = True)
    final_tweets_2.append(dataframe)
    time_likes_2 = pd.Series(data = dataframe.iloc[:,3].values, index = dataframe.iloc[:,2])
    time_likes_2.plot(figsize = (16,4), color = 'red', label = "likes", legend = True)
    summer_1 = 0
    for i in dataframe['sentiment']:
        summer_1+=i
    if summer_1>=num_tweets/5:
        print("the overall sentiment about %s is positive" %print_name)
    
    elif summer_1==num_tweets/5:
        print("the overall sentiment about %s is neutral" %print_name)
    else:
        print("the overall sentiment about %s is negative" %print_name)
        



tweets_new_1 = pd.DataFrame(final_tweets)
tweets_new_2 = pd.DataFrame(final_tweets_2)

tweets_new_1.to_csv("Twitter_by_username.csv")
tweets_new_2.to_csv("Twitter_by_hashtags.csv")