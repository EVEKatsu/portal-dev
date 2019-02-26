import settings
from initialize import db

class Tweet(db.Model):
    __tablename__ = 'tweets'

    id = db.Column(db.BigInteger, primary_key=True)
    category = db.Column(db.String, server_default=settings.DEFAULT_CATEGORY)
    user_id = db.Column(db.BigInteger)
    name = db.Column(db.String)
    screen_name = db.Column(db.String)
    text = db.Column(db.String)
    urls = db.Column(db.String)
    ban = db.Column(db.Boolean)
    profile_image_url_https = db.Column(db.String)
    created_at = db.Column(db.DateTime)
