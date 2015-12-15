from twitter import *
import time
import code

from twitter import *
import time
from streaming_helper import create_tweet_dictionary, create_user_dictionary, update_stream_sentiment
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment


def run(d):
    o_auth = OAuth(
        consumer_key=str(d['keys']['CONSUMER_KEY']),
        consumer_secret=str(d['keys']['CONSUMER_SECRET']),
        token=str(d['keys']['ACCESS_TOKEN']),
        token_secret=str(d['keys']['ACCESS_TOKEN_SECRET'])
    )

    t = Twitter(auth=o_auth)

    twitter_stream = TwitterStream(auth=o_auth, domain='userstream.twitter.com')

    metrics = dict()
    user_metrics = dict()
    tweet_metrics = dict()
    stream_sentiment = dict()

    while d['running']:
        for msg in twitter_stream.user():
            if (len(msg) > 1):
#                 print msg

                if 'user' in msg:
                    user = create_user_dictionary(msg)
                    user_metrics[user['name']] = user
                    print 'got user info'

                if 'text' in msg:
                    tweet = create_tweet_dictionary(msg)
                    tweet_metrics[tweet['id']] = tweet
                    stream_sentiment = update_stream_sentiment(stream_sentiment, tweet)
                    print 'got tweet info'

                metrics['tweet_metrics'] = tweet_metrics
                metrics['user_metrics'] = user_metrics
                metrics['stream_sentiment'] = stream_sentiment
                d['metrics'] = metrics
                print metrics
