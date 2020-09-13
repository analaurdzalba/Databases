#!/usr/bin/python

import tweepy
import json
import time
import sys
import glob
import pyodbc

server = 'localhost'
database = 'TwitterProject'
username = 'sa'
password = 'sqlDKS4sem2020'
driver='{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+password)
cursor = conn.cursor()
# TEST db connection
cursor.execute('SELECT * FROM RESEARCHERS')

for row in cursor:
    print(row)

# read all json files
file_str = r'bdatweets_*.json'
# list of pathnames according to above regex
file_lst = glob.glob(file_str)

# process every file
for file_idx, file_name in enumerate(file_lst):
    counter = 0
    with open(file_name, 'r') as f:
        for line in f:
            if counter == 0:
                # read researcher ID from the first line
                researcherID = int(line)
                counter = counter + 1
                continue
            if counter == 1:
                # read search ID from the second line
                searchID = int(line)
                counter = counter + 1
                continue
            if line != '\n':
                # each line is a tweet json object, load it and display user id
                tweet = json.loads(line)
                # user info
                userID = tweet['user']['id']
                verified = tweet['user']['verified']
                followers_count = tweet['user']['followers_count']
                # tweet info
                tweet_id = tweet['id']
                tweet_text = tweet['text']
                favorite_count = tweet['favorite_count']
                retweet_count = tweet['retweet_count']
                #hashtag objects
                hashtag_objects = tweet['entities']['hashtags']
                # read mentions information [indices, text]
                mentions = tweet['entities']['user_mentions']
                place_id = None
                #insert users
                rows = cursor.execute('SELECT * FROM USERS WHERE id = ?', userID).fetchall()
                if len(rows) == 0:
                    cursor.execute('''
                        INSERT INTO USERS (id, verified, followers_count)
                            VALUES
                                (?,?,?)
                    ''', (userID, verified, followers_count))
                    conn.commit()
                #insert place object
                place_object = tweet['place']
                if place_object:
                    place_id = place_object['id']
                    country = place_object['country_code']
                    city = place_object['name']
                    rows = cursor.execute('SELECT * FROM PLACES WHERE id = ?', place_id).fetchall()
                    if len(rows) == 0:
                        cursor.execute('''
                            INSERT INTO PLACES (id, country_code, name)
                                VALUES
                                    (?,?,?)
                        ''', (place_id, country, city))
                        conn.commit()
                else:
                    place_id = None;
                    country = None;
                    city = None;
                # insert tweet object *agregar variables
                rows = cursor.execute('SELECT * FROM TWEETS WHERE id = ?', tweet_id).fetchall()
                if len(rows) == 0:
                    cursor.execute('''
                        INSERT INTO TWEETS (id, tweet_text, "user", favorite_count, retweet_count, search_id, place_id)
                            VALUES
                                (?,?,?,?,?,?,?)
                    ''', (tweet_id, tweet_text, userID, favorite_count, retweet_count, searchID, place_id))
                    conn.commit()
                # insert hashtags
                for hashtag in hashtag_objects:
                    # insert only unique hashtags
                    rows = cursor.execute('''SELECT * FROM HASHTAGS WHERE tweet_id = ? AND
                            hashtag = ?''', (tweet_id, hashtag['text'])).fetchall()
                    if len(rows) == 0:
                        cursor.execute('''
                            INSERT INTO HASHTAGS (tweet_id, hashtag)
                                VALUES(?,?)
                        ''', (tweet_id, hashtag['text']))
                        conn.commit()
                # insert mentions
                for mention in mentions:
                    # insert only unique mentions
                    rows = cursor.execute('''SELECT * FROM MENTIONS WHERE tweet_id = ? AND
                            mention = ?''', (tweet_id, mention['screen_name'])).fetchall()
                    if len(rows) == 0:
                        cursor.execute('''
                            INSERT INTO MENTIONS (tweet_id, mention)
                                VALUES(?,?)
                        ''', (tweet_id, mention['screen_name']))
                        conn.commit()
cursor.close()
conn.close()
