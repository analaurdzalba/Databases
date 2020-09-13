#!/usr/bin/python
import tweepy
import json
import time
import sys
import os
import pyodbc

# override tweepy.StreamListener
from tweepy import API

class MyStreamListener(tweepy.StreamListener):

    def __init__(self, api=None):
        super(MyStreamListener, self).__init__(api)
        self.api = api or API()
        self.counter = 0
        self.researcherID = "3"
        self.searchID = "3"
        # define the filename with time as prefix
        self.output = open('bdatweets_%s.json'
                        % (time.strftime('%Y%m%d-%H%M%S')), 'a')
        # researcher ID and searchID
        self.output.write(self.researcherID+'\n'+self.searchID+'\n')
    def on_status(self, status):
        self.counter += 1
        json.dump(status._json, self.output)
        self.output.write('\n')
        if self.counter >= 500:
            self.output.close()
            self.output = open('bdatweets_%s.json'
                                % (time.strftime('%Y%m%d-%H%M%S')), 'a')
            # researcher ID and searchID
            self.output.write(self.researcherID+'\n'+self.searchID+'\n')
            self.counter = 0
        return

    def on_error(self, status):
        print(status)

from dotenv import load_dotenv
load_dotenv(dotenv_path='app.env', verbose=True)
consumer_key = os.getenv("CONSUMER_KEY")
print(consumer_key)
consumer_secret = os.getenv("CONSUMER_SECRET")
print(consumer_secret)
access_token = os.getenv("ACCESS_TOKEN")
print(access_token)
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
print(access_token_secret)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener(api))
print('Reading Twitter Stream...')
myStream.filter(track=['NBA','nba'],
    languages=["es", "en"],
    locations=[-122.75,36.8,-121.75,37.8,-74,40,-73,41])
#-122.75,36.8,-121.75,37.8,-74,40,-73,41
