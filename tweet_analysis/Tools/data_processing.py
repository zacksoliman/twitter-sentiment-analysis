import pandas as pd
import numpy as np
import string, re
import nltk
import time,random
import operator
#from tabulate import tabulate
from nltk.stem.snowball import SnowballStemmer

import os.path

stop_list = nltk.corpus.stopwords.words('english')
lemmatizer = nltk.stem.WordNetLemmatizer()
punctuation = list(string.punctuation)
stop_list = stop_list + punctuation +["rt", 'url']
stemmer = SnowballStemmer("english")
HillaryWords = ['hillary clinton','hillaryclinton','hilaryclinton','hillari clinton','hilari clinton','hilary clinton','hillary','clinton']
DonaldWords = ['donald trump','donaldtrump','donald','trump','realdonaldtrump']
CarsonWords = ['realbencarson','bencarson','carson','drbencarson']
BushWords = ['jebbush','bush','jeb']
HuckabeeWords = ['mike huckabee','huckabee','govmikehuckabee','huck']
RubioWords = ['marcorubio','marco rubio','rubio']
KasichWords = ['john kasich','johnkasich','kasich']
CruzWords = ['ted cruz','tedcruz','cruz']
hillary_re = re.compile('|'.join(map(re.escape, HillaryWords)))
donald_re = re.compile('|'.join(map(re.escape, DonaldWords)))
bush_re = re.compile('|'.join(map(re.escape, BushWords)))
carson_re = re.compile('|'.join(map(re.escape, CarsonWords)))
huckabee_re = re.compile('|'.join(map(re.escape, HuckabeeWords)))
rubio_re = re.compile('|'.join(map(re.escape, RubioWords)))
kasich_re = re.compile('|'.join(map(re.escape, KasichWords)))
cruz_re = re.compile('|'.join(map(re.escape, CruzWords)))

classifier =[]

def preprocess(tweet, lemmatize):

    if type(tweet)!=type(2.0):
        tweet = tweet.lower()
        tweet = " ".join(tweet.split('#'))
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        tweet = " ".join(tweet.split('@'))
        tweet = re.sub(r'@([^\s]+)', r'\1', tweet)
        tweet = re.sub('((www\.[^\s]+)|(https://[^\s]+))','URL',tweet)
        tweet = re.sub("http\S+", "URL", tweet)
        tweet = re.sub("https\S+", "URL", tweet)
        tweet = " ".join(tweet.split(':'))
        #removes @username from text entirely
        #tweet = re.sub('@[^\s]+','AT_USER',tweet)
        #tweet = tweet.replace("AT_USER","")
        tweet = tweet.replace("URL","")
        tweet = tweet.replace(".","")
        tweet = tweet.replace('\"',"")
        tweet = tweet.replace('&amp',"")
        #remove punctuation words
        tweet = " ".join([word for word in tweet.split(" ") if word not in stop_list])
        #remove words ending with special character
        tweet = " ".join([word for word in tweet.split(" ") if re.search('^[a-z]+$', word)])
        if lemmatize:
            #remove common words such as "the"
            tweet = " ".join([lemmatizer.lemmatize(word) for word in tweet.split(" ")])
            #stem similar words such as "hurt" and "hurting"
            tweet = " ".join([stemmer.stem(word) for word in tweet.split(" ")])
        tweet = re.sub('[\s]+', ' ', tweet)
        tweet = tweet.strip('\'"')
        #manually stem similar political words
        tweet = hillary_re.sub("hillary", tweet)
        tweet = donald_re.sub("donald", tweet)
        tweet = carson_re.sub("carson", tweet)
        tweet = bush_re.sub("bush", tweet)
        tweet = huckabee_re.sub("huckabee", tweet)
        tweet = cruz_re.sub("cruz", tweet)
        tweet = kasich_re.sub("kasich", tweet)
        tweet = rubio_re.sub("rubio", tweet)
    else:
        tweet=''
    return tweet

def clean_data(data, lemmatize):

    #text processing
    data['processed_text'] = data.text.apply(preprocess, lemmatize=lemmatize)
    #remove duplicate tweets
    data = data.drop_duplicates(subset='processed_text', keep='last')

    return data

def get_clean_data(dataset="Sentiment", lemmatize=True):

    basepath = os.path.dirname(__file__)
    filepath = os.path.abspath(os.path.join(basepath, "..", "data", dataset + ".csv"))
    data = pd.read_csv(filepath)

    return clean_data(data, lemmatize)