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


def main():
	d = dict()
	keys = dict()
	keys['CONSUMER_KEY'] = "aL8MuJFzmgCeHG9UL6POsPb8O"
	keys['CONSUMER_SECRET'] = "kpdLGCtnUnMRt80IBbrosAUwfMCqZ5P7K6OZNGSxcmSLj5TdSw"
	keys['ACCESS_TOKEN'] = "4266132851-zMFB5Uody378iP1tMBMr76oUQsFSQ4BNm0VtKOl"
	keys['ACCESS_TOKEN_SECRET'] = "yTPssEILIbGvJ8KZeXzVxItLDPGaFZ3hF8nRMR9Y73TQI"
	d['keys'] = keys
	d['running'] = True
	run(d)

if __name__ == '__main__':
    main()