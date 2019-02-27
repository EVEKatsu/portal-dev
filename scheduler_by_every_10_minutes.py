import os
from datetime import datetime
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


def update_tweets(category, query, filter_type=None):
    results = api.GetSearch(raw_query=query)
    
    for result in results:
        params = result.AsDict()
        user = User.query.filter(User.id == params['user']['id']).first()
        user_exists = user != None

        if filter_type == settings.SEARCH_EXCLUDE_KEYWORDS:
            text = params['text'].lower()
            if re.search(r'@[^ ]*eveonline[^ ]*', text):
                continue
            elif 'eveonline' in params['user']['screen_name'].lower() and not re.search(r'eve ?online', text):
                continue
        elif filter_type == settings.SEARCH_ONLY_INCLUDED_ID and not user_exists:
            continue

        tweet_exists = db.session.query(db.exists().where(Tweet.id == params['id'])).scalar()

        if 'retweeted_status' in params or params['user']['id'] in BAN_USERS or tweet_exists:
            continue

        if user_exists:
            user.updated_at = datetime.now()
        else:
            new_user = User(
                id=params['user']['id'],
                name=params['user']['name'],
                screen_name=params['user']['screen_name'],
                ban=False,
                profile_image_url_https=params['user']['profile_image_url_https'],
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            db.session.add(new_user)           

        tweet = Tweet(
            id=params['id'],
            category=category,
            user_id=params['user']['id'],
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
    for category, query, filter_type in settings.SEARCH_QUERIES:
        update_tweets(category, query, filter_type)
        db.session.commit()


if __name__ == "__main__":
    #update_tweets_test()
    main()
