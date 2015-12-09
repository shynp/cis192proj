from twitter import *
import time

def run(d):
	o_auth = OAuth(
		consumer_key=d['keys']['CONSUMER_KEY'],
		consumer_secret=d['keys']['CONSUMER_SECRET'],
		token=d['keys']['ACCESS_TOKEN'],
		token_secret=d['keys']['ACCESS_TOKEN_SECRET']
	)

	t = Twitter(auth=o_auth)

	twitter_stream = TwitterStream(auth=o_auth, domain='userstream.twitter.com')

	metrics = dict()
	user_metrics = dict()
	tweet_metrics = dict()

	for msg in twitter_stream.user():
		print msg

		if not d['running']:
			break

		# per tweet metrics
		tweet = dict()
		tweet['text'] = msg['text']
		tweet['user'] = msg['user']['name'] # who posted the tweet
		tweet['favorite_count'] = msg['favorite_count'] # how many likes it has
		tweet['retweet_count'] = msg['retweet_count'] # how many retweets it has
		tweet_metrics[tweet['text']] = tweet

		#  per user metrics
		user = dict()
		user['name'] = msg['user']['name']
		user['favorite_count'] = msg['user']['favourites_count']
		user['status_count'] = msg['user']['statuses_count']
		user['follower_count'] = msg['user']['followers_count']
		user['following_count'] = msg['user']['friends_count']
		user_metrics[user['name']] = user

		# TODO include metrics bucketed into groups, a la competitors, followers, etc.

		metrics['tweet_metrics'] = tweet_metrics
		metrics['user_metrics'] = user_metrics
		d['metrics'] = metrics


