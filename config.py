#!/usr/local/bin/python3

search_query = 'bumblebee'
filename = search_query + '_search.csv'

maxTweets = 100   # Some arbitrary large number
tweetsPerQry = 50 # 100  is the max the API permits

# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1

