import os
from datetime import datetime

import twitter

import settings
from initialize import app, db
from models import Tweet

api = twitter.Api(
    consumer_key=os.environ["CONSUMER_KEY"],
    consumer_secret=os.environ["CONSUMER_SECRET"],
    access_token_key=os.environ["ACCESS_TOKEN_KEY"],
    access_token_secret=os.environ["ACCESS_TOKEN_SECRET"],
)

BAN_USERS = [108954366, 2841563053]

def update_tweets(category, query):
    results = api.GetSearch(raw_query='q=' + query + settings.DEFAULT_SEARCH_QUERY)

    for result in results:
        params = result.AsDict()
        exists = db.session.query(db.exists().where(Tweet.id == params['id'])).scalar()

        if 'retweeted_status' in params or params['user']['id'] in BAN_USERS or exists:
            continue

        # category = 'misc'
        # included_hashtag_keys = []
        # for hashtag in params['hashtags']:
        #     if not 'text' in hashtag:
        #         continue

        #     included_hashtag_keys.append(hashtag['text'].lower())

        # for hashtag_key in ['evejapan', 'eveonline']:
        #     if hashtag_key in included_hashtag_keys:
        #         category = hashtag_key
        #         break

        # if category == 'misc':
        #     print(params['hashtags'], params['text'])
        tweet = Tweet(
            id=params['id'],
            category=category,
            user_id=params['user']['id'],
            name=params['user']['name'],
            screen_name=params['user']['screen_name'],
            urls=str(params['urls']),
            text=params['text'],
            ban=False,
            profile_image_url_https=params['user']['profile_image_url_https'],
            created_at=params['created_at'],
        )
        db.session.add(tweet)

if __name__ == "__main__":
    for category, query in settings.SEARCH_QUERIES:
         update_tweets(category, query)

    # q = settings.SEARCH_QUERIES[0]
    # update_tweets(q[0], q[1])

    tweets = Tweet.query.order_by(Tweet.created_at.desc()).offset(1000)
    for tweet in tweets:
        Tweet.query.filter(Tweet.id == tweet.id).delete()

    db.session.commit()
