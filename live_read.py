#!/usr/local/bin/python3

# live_read.py reads from the twitter sream for tweets using a certain keyword 
# it puts them to std out and to a csv file

import tweepy
import csv
import sys
from datetime import datetime
from twitter_authentication import *
from config import *

if len(sys.argv) >= 2:
    search_query = sys.argv[1]
    filename = sys.argv[2]

# auth & api handlers
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

print('Authenticated as %s' % api.me().screen_name)

# create output file and add header
with open(filename, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    header = ['id_str','in_reply_to_status_id_str','in_reply_to_user_id_str','created_at','in_reply_to_screen_name','source','user_name','user_screen_name','user_created_at','user_statuses_count','user_description','user_location','user_verified','user_followers_count','user_friends_count','user_url','text','entities_hashtags','entities_urls','entities_user_mentions']
    writer.writerow(header)
    print( "Hopefully, created file %s" % filename)

# function to encode to UTF-8
def enc8(v):
    if isinstance(v,list):
        v = [enc8(i) for i in v]
    else:
        try: 
            v.encode('UTF-8')
        except:
            v
    return v
																		    
# function for adding data to csv file
def write_csv(row_data, filename):
    #row_data = [enc8(d) for d in row_data]
    with open(filename, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(row_data)

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        writable = [
                    status.id_str, 
                    status.in_reply_to_status_id_str, 
                    status.in_reply_to_user_id_str, 
                    status.created_at, status.in_reply_to_screen_name, 
                    status.source, status.user._json['name'], 
                    status.user._json['screen_name'], status.user._json['created_at'], 
                    #status.user._json['statuses_count'], 
                    status.user._json['description'], 
                    status.user._json['location'], 
                    #status.user._json['verified'], status.user._json['followers_count'],  
                    #status.user._json['friends_count'], status.user._json['url'],
                    status.text, status.entities['hashtags'], 
                    #status.entities['urls'], status.entities['user_mentions']
                    ]
        print(writable)
        write_csv( writable, filename)

	# all parameters possible here:
	# https://dev.twitter.com/overview/api/tweets
	# status.id_str.encode('UTF-8')

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

# generate stream by search term
myStream.filter(track=search_query)

