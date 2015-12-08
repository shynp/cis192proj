from twitter import *
import time

# CONSUMER_KEY = "aL8MuJFzmgCeHG9UL6POsPb8O"
# CONSUMER_SECRET = "kpdLGCtnUnMRt80IBbrosAUwfMCqZ5P7K6OZNGSxcmSLj5TdSw"
# ACCESS_TOKEN = "4266132851-zMFB5Uody378iP1tMBMr76oUQsFSQ4BNm0VtKOl"
# ACCESS_TOKEN_SECRET = "yTPssEILIbGvJ8KZeXzVxItLDPGaFZ3hF8nRMR9Y73TQI"

# o_auth = OAuth(
# 		consumer_key=CONSUMER_KEY,
# 		consumer_secret=CONSUMER_SECRET,
# 		token=ACCESS_TOKEN,
# 		token_secret=ACCESS_TOKEN_SECRET
# 	)




def run(d):
	CONSUMER_KEY = d['keys']['CONSUMER_KEY']
	CONSUMER_SECRET = "kpdLGCtnUnMRt80IBbrosAUwfMCqZ5P7K6OZNGSxcmSLj5TdSw"
	ACCESS_TOKEN = "4266132851-zMFB5Uody378iP1tMBMr76oUQsFSQ4BNm0VtKOl"
	ACCESS_TOKEN_SECRET = "yTPssEILIbGvJ8KZeXzVxItLDPGaFZ3hF8nRMR9Y73TQI"

	o_auth = OAuth(
		consumer_key=CONSUMER_KEY,
		consumer_secret=CONSUMER_SECRET,
		token=ACCESS_TOKEN,
		token_secret=ACCESS_TOKEN_SECRET
	)

	t = Twitter(auth=o_auth)

	twitter_stream = TwitterStream(auth=o_auth, domain='userstream.twitter.com')

	for msg in twitter_stream.user():
		if not d['running']:
			break


