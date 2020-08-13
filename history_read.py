#!/usr/local/bin/python3

# history_read.py searches for recent records, based on a key and writes them to a csv

import tweepy
import csv
import sys
import os
from twitter_authentication import *
from config import *

if len(sys.argv) >= 2:
    search_query = sys.argv[1]
    filename = sys.argv[2]

# auth & api handlers
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

api = tweepy.API(auth)


# create output file and add header
with open(filename, 'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    header = ['id_str','in_reply_to_status_id_str','in_reply_to_user_id_str','created_at','in_reply_to_screen_name','source','user_name','user_screen_name','user_created_at','user_statuses_count','user_description','user_location','user_verified','user_followers_count','user_friends_count','user_url','text','entities_hashtags','entities_urls','entities_user_mentions']
    writer.writerow(header)

# function for adding data to csv file
def write_csv(row_data, filename):
    with open(filename, 'a', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(row_data)


tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
while tweetCount < maxTweets:
    try:
        if (max_id <= 0):
            if (not sinceId):
                new_tweets = api.search(q=search_query, count=tweetsPerQry)
            else:
                new_tweets = api.search(q=search_query, count=tweetsPerQry,
                                        since_id=sinceId)
        else:
            if (not sinceId):
                new_tweets = api.search(q=search_query, count=tweetsPerQry,
                                        max_id=str(max_id - 1))
            else:
                new_tweets = api.search(q=search_query, count=tweetsPerQry,
                                        max_id=str(max_id - 1),
                                        since_id=sinceId)
        if not new_tweets:
            print("No more tweets found")
            break
        for status in new_tweets:
            write_csv([status.id_str, status.in_reply_to_status_id_str, 
                       status.in_reply_to_user_id_str, status.created_at, status.in_reply_to_screen_name, 
                       status.source, status.user._json['name'], status.user._json['screen_name'], 
                       status.user._json['created_at'], status.user._json['statuses_count'], 
                       status.user._json['description'], status.user._json['location'], 
                       status.user._json['verified'], status.user._json['followers_count'],  
                       status.user._json['friends_count'], status.user._json['url'], status.text, 
                       status.entities['hashtags'], status.entities['urls'], 
                       status.entities['user_mentions'] 
                       ], 
                       filename)
        tweetCount += len(new_tweets)
        print("Downloaded {0} tweets".format(tweetCount))
        max_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # Just exit if any error
        print("some error : " + str(e))
        break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, filename))
