import os
import datetime
import re

import twitter

import settings
from initialize import app, db
from models import Tweet, User

api = twitter.Api(
    consumer_key=os.environ["CONSUMER_KEY"],
    consumer_secret=os.environ["CONSUMER_SECRET"],
    access_token_key=os.environ["ACCESS_TOKEN_KEY"],
    access_token_secret=os.environ["ACCESS_TOKEN_SECRET"],
)

BAN_USERS = [
    108954366, # @admiralnel
    2841563053, # @mmo_anti_oni
    2485360038, # @EVE_dokuimo
]


def update_tweets(category, query, exclude_keyword, only_included_ids):
    results = api.GetSearch(raw_query=query)

    for result in results:
        params = result.AsDict()
        user = User.query.filter(User.id == params['user']['id']).first()
        user_exists = user != None

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
    from settings import DEFAULT_SEARCH_QUERY, SEARCH_EXCLUDE_KEYWORDS, SEARCH_ONLY_INCLUDED_ID
    query = 'q=eve' + DEFAULT_SEARCH_QUERY
    update_tweets('test', query, None)
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
    #update_tweets_test()
    main()
