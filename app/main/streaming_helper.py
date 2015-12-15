from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
import unicodedata

def create_tweet_dictionary(msg):
    tweet = dict()
    tweet['id'] = msg['id']
    tweet['text'] = msg['text']
    tweet['user'] = msg['user']['name']
    tweet['retweet_count'] = msg['retweet_count']
    tweet['favorite_count'] = msg['favorite_count']
    tweet['timestamp_ms'] = msg['timestamp_ms']
    tweet['datetime'] = msg['created_at']

    print("type of:")
    print(type(unicodedata.normalize('NFKD', tweet['text']).encode('ascii','ignore')))
    tweet_sentiment = vaderSentiment(unicodedata.normalize('NFKD', tweet['text']).encode('ascii','ignore'))
    tweet['pos_sentiment'] = tweet_sentiment['pos']
    tweet['neu_sentiment'] = tweet_sentiment['neu']
    tweet['neg_sentiment'] = tweet_sentiment['neg']
    return tweet


def create_user_dictionary(msg):
    user = dict()
    user['id'] = msg['user']['id']
    user['name'] = msg['user']['name']
    user['status_count'] = msg['user']['statuses_count']
    user['follower_count'] = msg['user']['followers_count']
    user['following_count'] = msg['user']['friends_count']
    user['favorite_count'] = msg['user']['favourites_count']
    return user


# used to update current sentiment score with new tweet
def update_stream_sentiment(stream_sentiment, tweet):
    sentiments = ['pos_sentiment', 'neu_sentiment', 'neg_sentiment']
    print ("pos sentiment of tweet: " + str(tweet['pos_sentiment']))
    print ("neu sentiment of tweet: " + str(tweet['neu_sentiment']))
    print ("neg sentiment of tweet: " + str(tweet['neg_sentiment']))

    if ('num_tweets' not in stream_sentiment):
        stream_sentiment['num_tweets'] = 1
        for s in sentiments:
            stream_sentiment[s] = tweet[s]
    else:
        stream_sentiment['num_tweets'] += 1
        for s in sentiments:
            stream_sentiment[s] = (stream_sentiment[s] *
                                   (stream_sentiment['num_tweets'] - 1) + tweet[s]) \
                                    / stream_sentiment['num_tweets']
    return stream_sentiment
