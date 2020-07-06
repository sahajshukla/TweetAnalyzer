# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 18:29:31 2020

@author: Sahaj
"""

from twitter_analysis import *
data = final_tweets
import re
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import string
import nltk
import warnings 
warnings.filterwarnings("ignore", category=DeprecationWarning)
from nltk.stem.porter import *
from wordcloud import WordCloud

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
        
    return input_txt

for tweet_obj in final_tweets:
    tweet_obj['tidy_tweet'] = np.vectorize(remove_pattern)(tweet_obj.iloc[:,0], "@[\w]*")
    tweet_obj['tidy_tweet'] = tweet_obj['tidy_tweet'].str.replace("[^a-zA-Z#]", " ")
    tweet_obj['tidy_tweet'] = tweet_obj['tidy_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))
    tokenized_tweet = tweet_obj['tidy_tweet'].apply(lambda x: x.split())


stemmer = PorterStemmer()

tokenized_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x]) # stemming
tokenized_tweet.head()

for i in range(len(tokenized_tweet)):
    tokenized_tweet[i] = ' '.join(tokenized_tweet[i])

for tweet_obj in final_tweets:
    tweet_obj['tidy_tweet'] = tokenized_tweet

    all_words = ' '.join([text for text in tweet_obj['tidy_tweet']])
    wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)

    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()


