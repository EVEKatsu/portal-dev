import os
from datetime import datetime
import re

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

URL_PATTERN = r'https?:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+'
EXLUDE_TEXT_PATTEN = r'@[^ ]*eve ?online[^ ]*'


def update_tweets(category, query, exlude):
    results = api.GetSearch(raw_query='q=' + query + settings.DEFAULT_SEARCH_QUERY)
    for result in results:
        params = result.AsDict()

        if exlude:
            if 'eveonline' in params['user']['screen_name'].lower() or re.search(EXLUDE_TEXT_PATTEN, params['text'].lower()):
                continue

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


def update_tweets_test(query_index):
    q = settings.SEARCH_QUERIES[query_index]
    update_tweets('test', q[1], True)
    db.session.commit()


def main():
    for category, query in settings.SEARCH_QUERIES:
         update_tweets(category, query)
         db.session.commit()

    # q = settings.SEARCH_QUERIES[0]
    # update_tweets(q[0], q[1])

    tweets = Tweet.query.order_by(Tweet.created_at.desc()).offset(1000)
    for tweet in tweets:
        Tweet.query.filter(Tweet.id == tweet.id).delete()

    db.session.commit()


if __name__ == "__main__":
    main()
