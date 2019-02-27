import settings
from initialize import app, db
from models import Tweet, User


def main():
    tweets = Tweet.query.order_by(Tweet.created_at.desc()).offset(settings.TWEETS_MAXIMUM_LIMIT)
    for tweet in tweets:
        db.session.delete(tweet)

    included_users = {}
    for tweet in Tweet.query:
        if tweet.user_id not in included_users:
            included_users[tweet.user_id] = {
                'name': tweet.user_name,
                'screen_name': tweet.user_screen_name,
                'description': tweet.user_description,
                'profile_image_url_https': tweet.user_profile_image_url_https,
            }

    for user in User.query:
        if user.id in included_users:
            included_user = included_users[user.id]
            user.name = included_user['name']
            user.screen_name = included_user['screen_name']
            user.description = included_user['description']
            user.profile_image_url_https = included_user['profile_image_url_https']
        else:
            db.session.delete(user)

    db.session.commit()


if __name__ == "__main__":
    main()
