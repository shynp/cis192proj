from twitter import *
import time
import code

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

	# code.interact(local=locals())
	for msg in twitter_stream.user():
		print msg

		if not d['running']:
			break

		# per tweet metrics
		tweet = dict()

		#  per user metrics
		user = dict()

		if 'text' in msg:
			tweet['text'] = msg['text']
		if 'user' in msg:
			tweet['user'] = msg['user']['name'] # who posted the tweet
			user['name'] = msg['user']['name']
			user['status_count'] = msg['user']['statuses_count']
			user['follower_count'] = msg['user']['followers_count']
			user['following_count'] = msg['user']['friends_count']
			user_metrics[user['name']] = user
		if 'favorite_count' in msg:
			tweet['favorite_count'] = msg['favorite_count'] # how many likes it has
			user['favorite_count'] = msg['user']['favourites_count']
		if 'retweet_count' in msg:
			tweet['retweet_count'] = msg['retweet_count'] # how many retweets it has
		if 'text' in msg:
			tweet_metrics[tweet['text']] = tweet

		# TODO include metrics bucketed into groups, a la competitors, followers, etc.

		metrics['tweet_metrics'] = tweet_metrics
		metrics['user_metrics'] = user_metrics
		d['metrics'] = metrics
