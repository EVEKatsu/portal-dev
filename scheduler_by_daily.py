import settings
from initialize import app, db
from models import Tweet, User


def main():
    tweets = Tweet.query.order_by(Tweet.created_at.desc()).offset(settings.MAXIMUM_LIMIT_TWEETS)
    for tweet in tweets:
        Tweet.query.filter(Tweet.id == tweet.id).delete()

    users = User.query.order_by(User.updated_at.desc()).offset(settings.MAXIMUM_LIMIT_USERS)
    for user in users:
        User.query.filter(User.id == user.id).delete()

    db.session.commit()


if __name__ == "__main__":
    #update_tweets_test('q=eveonline')
    main()
