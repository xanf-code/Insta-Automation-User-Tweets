import tweepy
import configparser
import pandas as pd
import json

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# user tweets
user = 'Positive_Call'
limit=200

tweets = tweepy.Cursor(api.user_timeline, screen_name=user, count=limit, tweet_mode='extended' ).items(limit)

# tweets = api.user_timeline(screen_name=user, count=limit, tweet_mode='extended')

# create DataFrame
columns = ['Count', 'Tweet']
data = []
count=1

for tweet in tweets:
    if ('RT @' not in tweet.full_text) and ('https://' not in tweet.full_text) and ('http://' not in tweet.full_text) and ('#' not in tweet.full_text) and ('@' not in tweet.full_text) and (':' not in tweet.full_text):
        data.append([count, tweet.full_text])
        count+=1

df = pd.DataFrame(data, columns=columns)
d = df.to_dict(orient='records')
j = json.dumps(d)

with open('tweets.json', 'w') as f:
    f.write(j)
