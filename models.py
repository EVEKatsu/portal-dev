import settings
from initialize import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String)
    screen_name = db.Column(db.String)
    description = db.Column(db.String)
    profile_image_url_https = db.Column(db.String)
    tweets_count = db.Column(db.Integer)
    tweets = db.relationship('Tweet', backref='user', lazy=True)

class Tweet(db.Model):
    __tablename__ = 'tweets'

    id = db.Column(db.BigInteger, primary_key=True)
    category = db.Column(db.String, server_default=settings.DEFAULT_CATEGORY)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user_name = db.Column(db.String)
    user_screen_name = db.Column(db.String)
    user_description = db.Column(db.String)
    user_profile_image_url_https = db.Column(db.String)
    ban = db.Column(db.Boolean)
    text = db.Column(db.String)
    created_at = db.Column(db.DateTime)
