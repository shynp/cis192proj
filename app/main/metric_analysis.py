from heapq import nlargest


# gets all tweets (dictionaries) from a specified user
def list_all_tweets_from_user(username, tweet_metrics):
    list_of_tweets = []
    for tweet in tweet_metrics:
        if username == tweet_metrics[tweet]['user']:
            list_of_tweets.append(tweet_metrics[tweet])
    return list_of_tweets


# gets all users that have tweeted
def list_all_users(user_metrics):
    list_of_users = []
    for _, user in user_metrics:
        list_of_users.append(user)
    return list_of_users


# returns a list of tweets based on a given set of inputs
def get_tweets_ranked(list_of_tweets, num_results=10, ranking_type='retweet_count'):
    allowed_ranking_types = ['retweet_count', 'favorite_count', 'timestamp_ms']
    if (ranking_type not in allowed_ranking_types):
        return None
    return nlargest(num_results, list_of_tweets, key=lambda tweet: tweet[ranking_type])


# returns a list of users based on a given set of inputs
def get_users_ranked(list_of_users, num_results=10, ranking_type='friends'):
    allowed_ranking_types = ['following_count', 'follower_count',
                             'status_count', 'favorite_count']
    if (ranking_type not in allowed_ranking_types):
        return None
    return nlargest(num_results, list_of_users, key=lambda user: user[ranking_type])


# graph of sentiments over time
def get_user_sentiment(user_name, tweet_metrics):
    sentiment = dict()
    sentiment['pos_sentiment'] = 0.0
    sentiment['neu_sentiment'] = 0.0
    sentiment['neg_sentiment'] = 0.0
    count_of_tweets = 0
    for tweet in tweet_metrics:
        if user_name is tweet['user']:
            count_of_tweets += 1
            for s in sentiment:
                sentiment[s] += tweet[s]
    for s in sentiment:
        sentiment[s] /= count_of_tweets
    return sentiment
