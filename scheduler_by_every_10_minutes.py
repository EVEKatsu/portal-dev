import os
import datetime
import re
import json
import urllib.parse

from requests_oauthlib import OAuth1Session

import settings
from initialize import app, db
from models import Tweet, User

twitter = OAuth1Session(
    os.environ["CONSUMER_KEY"],
    os.environ["CONSUMER_SECRET"],
    os.environ["ACCESS_TOKEN_KEY"],
    os.environ["ACCESS_TOKEN_SECRET"],
)

BAN_USERS = [
    108954366, # @admiralnel
    2841563053, # @mmo_anti_oni
    2485360038, # @EVE_dokuimo
]

SEARCH_API_URL = "https://api.twitter.com/1.1/search/tweets.json"


def update_tweets(category, search_words, exclude_keyword, only_included_ids):
    search_params = settings.DEFAULT_SEARCH_PARAMS.copy()
    search_params['q'] = search_words + ' exclude:retweets'
    requests = twitter.get(SEARCH_API_URL, params=search_params)

    if requests.status_code != 200:
        print('!!!!!ERROR!!!!! - %d' % requests.status_code)
        return

    for params in json.loads(requests.text)['statuses']:
        user = User.query.filter(User.id == params['user']['id']).first()
        user_exists = user is not None

        if exclude_keyword:
            screen_name = params['user']['screen_name'].lower()
            text = params['text'].lower()

            if re.search(r'@[^ ]*' + exclude_keyword, text) or re.search(exclude_keyword, screen_name):
                if not re.search(r' [^@ ]*' + exclude_keyword, ' ' + text):
                    continue

        if only_included_ids and not user_exists:
            continue

        tweet_exists = db.session.query(db.exists().where(Tweet.id == params['id'])).scalar()

        if 'retweeted_status' in params or params['user']['id'] in BAN_USERS or tweet_exists:
            continue

        description = ''
        if 'description' in params['user']:
            description = params['user']['description']

        if not user_exists:
            new_user = User(
                id=params['user']['id'],
                name=params['user']['name'],
                screen_name=params['user']['screen_name'],
                description=description,
                profile_image_url_https=params['user']['profile_image_url_https'],
                tweets_count=0
            )
            db.session.add(new_user)

        tweet = Tweet(
            id=params['id'],
            category=category,
            user_id=params['user']['id'],
            user_name=params['user']['name'],
            user_screen_name=params['user']['screen_name'],
            user_description=description,
            user_profile_image_url_https=params['user']['profile_image_url_https'],
            ban=False,
            text=params['text'],
            created_at=params['created_at'],
        )
        db.session.add(tweet)


def update_tweets_test():
    update_tweets('zkillboard', 'zkillboard.com lang:ja', None, False)
    db.session.commit()


def main():
    for category, query, exclude_keyword, only_included_ids in settings.SEARCH_QUERIES:
        update_tweets(category, query, exclude_keyword, only_included_ids)

    User.query.update({'tweets_count': 0})
    limit_datetime = datetime.datetime.now() - datetime.timedelta(days=settings.DEADLINE_DAYS)
    count_dict = {}
    for tweet in Tweet.query.filter(Tweet.created_at > limit_datetime):
        if tweet.user_id not in count_dict:
            count_dict[tweet.user_id] = 0

        count_dict[tweet.user_id] += 1

    for key, val in count_dict.items():
        User.query.filter(User.id == key).first().tweets_count = val

    db.session.commit()

if __name__ == "__main__":
    if settings.DEBUG:
        update_tweets_test()
        #main()
    else:
        main()
