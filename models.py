import settings
from initialize import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String)
    screen_name = db.Column(db.String)
    ban = db.Column(db.Boolean)
    profile_image_url_https = db.Column(db.String)
    tweets = db.relationship('Tweet', backref='user', lazy=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

class Tweet(db.Model):
    __tablename__ = 'tweets'

    id = db.Column(db.BigInteger, primary_key=True)
    category = db.Column(db.String, server_default=settings.DEFAULT_CATEGORY)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    ban = db.Column(db.Boolean)
    text = db.Column(db.String)
    created_at = db.Column(db.DateTime)
