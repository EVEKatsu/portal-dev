import os
from datetime import datetime

import twitter

from database import app, db
from models import Tweet

api = twitter.Api(
    consumer_key=os.environ["CONSUMER_KEY"],
    consumer_secret=os.environ["CONSUMER_SECRET"],
    access_token_key=os.environ["ACCESS_TOKEN_KEY"],
    access_token_secret=os.environ["ACCESS_TOKEN_SECRET"],
)

BAN_USERS = [108954366, 2841563053]

if __name__ == "__main__":
    results = api.GetSearch(raw_query="q=%23evejapan&src=typd&count=100")

    for result in results:
        params = result.AsDict()
        exists = db.session.query(db.exists().where(Tweet.id == params['id'])).scalar()

        if 'retweeted_status' in params or params['user']['id'] in BAN_USERS or exists:
            continue

        tweet = Tweet(
            id=params['id'],
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

    tweets = Tweet.query.order_by(Tweet.created_at.desc()).offset(1000)
    for tweet in tweets:
        Tweet.query.filter(Tweet.id == tweet.id).delete()

    db.session.commit()
