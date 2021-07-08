import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import logging
from config_si_uu import Twitter # storage for authentification
import pymongo
import time

time.sleep(15) # seconds

client = pymongo.MongoClient("mongodb")
db = client.lyrics

##### SECTION 1: Authentication #######
#######################################
consumer_key = Twitter['consumer_key']
consumer_secret = Twitter['consumer_secret']
access_token = Twitter['access_token']
access_token_secret = Twitter['access_token_secret']

AUTH = tweepy.OAuthHandler(consumer_key, consumer_secret)

## user authentification
AUTH.set_access_token(Twitter['access_token'], Twitter['access_token_secret'])

### SECTION 2: ACCESSING REST API #####
#######################################
## access to REST Api (no streaming)
api = tweepy.API(AUTH, wait_on_rate_limit=True)
user = api.me()
logging.critical("connection established with user: " + user.name)

with open("output_tweets.txt", "w") as f:
    f.write(user.status.text)
    f.write(str(user.status.created_at))

class TwitterListener(StreamListener):

    def on_data(self, data):

        """
        Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time

        By default it's using the data from the api user timeline.
        """

        t = json.loads(data) #t is just a regular python dictionary.

        tweet = {
        'text': t['text'],
        'username': t['user']['screen_name'],
        'followers_count': t['user']['followers_count']
        }

        logging.critical(f'\n\n\nTWEET INCOMING: {tweet["text"]}\n\n\n')

        def on_error(self, status):
            if status == 420:
                print(status)
            return False

        with open('live_tweets.txt','a') as tf:
            tf.write(t['text'])
        return True

    #def __init__(self, num_tweets_to_grab):
    #    self.counter = 0
    #    self.num_tweets_to_grab = num_tweets_to_grab


    def __init__(self, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        self.saveFile = open('live_tweets.txt', 'a')
        super(TwitterListener, self).__init__()

    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            self.saveFile.write(data)
            self.saveFile.write('\n')
            return True
        else:
            self.saveFile.close()
            return False

stream = Stream(AUTH, TwitterListener(time_limit=20))
stream.filter(track=['Ghana'], languages=['en'])


#listener = TwitterListener()
#stream = Stream(AUTH, listener)

#stream = Stream(AUTH, TwitterListener(num_tweets_to_grab=10))
#stream.filter(track=['Ghana'], languages=['en'])
