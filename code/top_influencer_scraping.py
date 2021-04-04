# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 11:46:28 2019

@author: ruite
"""

import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials
consumer_key = "kDT9bOaRYL7bx1oUAYsxh9auu" 
consumer_secret = "3vO7gtgfXcDQFALxWY4cLwtJJZdlsmh2Em0Df62hnhqWaF5iB4"
access_key = "940867989527846912-08JoDAlHgV2k0rQ7j2vyWxakqyVFl27"
access_secret = "ufydwkINFdcgtfPkQ2W9zjlPKqaCwwK6aJ22IyaLCcPjp"


def get_all_tweets(screen_name):
        #Twitter only allows access to a users most recent 3240 tweets with this method

        #authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)

        #initialize a list to hold all the tweepy Tweets
        alltweets = []

        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = screen_name,count=1)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
                print ("getting tweets before %s" % (oldest))

                #all subsequent requests use the max_id param to prevent duplicates
                new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

                #save most recent tweets
                alltweets.extend(new_tweets)

                #update the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1

                print ("...%s tweets downloaded so far" % (len(alltweets)))
        
        #go through all found tweets and remove the ones with no images 
        outtweets = [] #initialize master list to hold our ready tweets
        #for tweet in alltweets:
        i = 0
        while len(outtweets) <= 50 and i <= len(alltweets)-1:
                tweet = alltweets[i]
                #not all tweets will have media url, so lets skip them
                try:
                        print (tweet.entities['media'][0]['media_url'])
                except (NameError, KeyError):
                        #we dont want to have any entries without the media_url so lets do nothing
                        pass
                else:
                        #got media_url - means add it to the output
                        outtweets.append([tweet.id_str, tweet.text.encode("utf-8"), tweet.entities['media'][0]['media_url'],screen_name])
                i += 1

        with open('/Users/junkangzhang/Downloads/MMA 2019/Courses/INSY670/Final/top_tweets.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(['id',"text","media_url",'user_name'])
                writer.writerows(outtweets)

        pass



import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
### select top 20 car-related accounts with max 50 image per account
users = pd.read_csv('/Users/junkangzhang/Downloads/MMA 2019/Courses/INSY670/Final/filtered_top100.csv')
users = users.drop(users.columns.tolist()[0],axis=1)
users = users[users.related == 'yes']
users = users.reset_index(drop=True)
topusers = users.iloc[:10,:]

### Scrap urls
for i in topusers.user_name:
    get_all_tweets(i)

df = pd.read_csv('/Users/junkangzhang/Downloads/MMA 2019/Courses/INSY670/Final/top_tweets.csv')
df = df[df.id != 'id']

df = df.dropna(how='all')
df['#_likes'] = ''
df['#_comments'] = ''
df['#_retweets'] = ''

df = df.reset_index(drop=True)

for i in range(len(df)):
    html = requests.get('https://twitter.com/' + str(df['user_name'].loc[i]) + '/status/' + str(df['id'].loc[i]))
    soup = BeautifulSoup(html.text, 'lxml')
    likes = soup.find_all('span', attrs={'class':'ProfileTweet-actionCountForAria'})[2].contents
    retweets = soup.find_all('span', attrs={'class':'ProfileTweet-actionCountForAria'})[1].contents
    reply = soup.find_all('span', attrs={'class':'ProfileTweet-actionCountForAria'})[0].contents
    df['#_likes'].loc[i] = likes
    df['#_comments'].loc[i] = reply
    df['#_retweets'].loc[i] = retweets 

df['likes'] = [re.sub("[^0-9]", "",i[0]) for i in df['#_likes']]
df['comments'] = [re.sub("[^0-9]", "",i[0]) for i in df['#_comments']]
df['retweets'] = [re.sub("[^0-9]", "",i[0]) for i in df['#_retweets']]

df = df.drop(['#_likes','#_comments','#_retweets'],axis=1)
df.to_csv('/Users/junkangzhang/Downloads/MMA 2019/Courses/INSY670/Final/url_file.csv')   

df = pd.read_csv('/Users/junkangzhang/Downloads/MMA 2019/Courses/INSY670/Final/url_file.csv')