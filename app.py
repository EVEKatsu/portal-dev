import datetime
import re

from flask import Flask, render_template
from flask_sqlalchemy import Pagination

import settings
from initialize import app, db
from models import Tweet, User

URL_PATTERN = r'https?:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+'

def default_kwargs():
  return {
    'SITENAME': 'イブカツ！',
    'SITEURL': 'https://evekatsu.herokuapp.com',
    'DATETIME': datetime.datetime.now(),
    'VERSION': settings.VERSION,
    'MENUITEMS': (
      ('プレイヤー', 'users'),
      ('ツイッター', 'tweets'),
      ('ブログ', 'articles'),
      ('動画', 'videos'),
      ('ランキング', 'ranking'),
    ),
  }

def default_render(template_name_or_list, kwargs={}):
  return render_template(template_name_or_list, **{**default_kwargs(), **kwargs})

@app.route("/")
def index():
  return default_render('index.html')

@app.route('/users', defaults={'page': 1})
@app.route("/users/<int:page>")
def users(page):
  kwargs = {}
  kwargs['users'] = User.query.order_by(User.tweets_count.desc()). \
                    paginate(page, settings.USERS_PER_PAGE)

  return default_render('users.html', kwargs)

@app.route('/user/<int:user_id>', defaults={'page': 1})
@app.route("/user/<int:user_id>/<int:page>")
def user(user_id, page):
  user = User.query.filter(User.id == user_id).first()
  name = '%s(%s)さん' % (user.name, user.screen_name)
  kwargs = {
    'ENDPOINT': 'user',
    'TITLE': name,
    'DESCRIPTION': name + 'のEVE Onlineについてのツイートです',
    'pagination_kwargs': {
      'user_id': user_id,
    },
  }

  kwargs['tweets'] =  Tweet.query.filter(Tweet.user_id == user_id). \
                      order_by(Tweet.created_at.desc()). \
                      paginate(page, settings.TWEETS_PER_PAGE)

  return default_render('tweets.html', kwargs)

@app.route('/tweets', defaults={'submenu': 'all', 'page': 1})
@app.route("/tweets/<string:submenu>/<int:page>")
def tweets(submenu, page):
  category = submenu
  kwargs = {
    'ENDPOINT': 'tweets',
    'TWEETS_MENUITEMS': (
      ('すべて', 'all'),
      ('#evejapan', 'evejapan'),
      ('#eveonline', 'eveonline'),
      ('その他', 'misc'),
    ),
    'category': category,
    'pagination_kwargs': {
      'submenu': category,
    },
  }

  if category == 'all':
    query = Tweet.query
  else:
    query = Tweet.query.filter(Tweet.category == category)

  limit_datetime = datetime.datetime.now() - datetime.timedelta(days=settings.DEADLINE_DAYS)
  kwargs['tweets'] =  query.filter(Tweet.created_at > limit_datetime). \
                      order_by(Tweet.created_at.desc()). \
                      paginate(page, settings.TWEETS_PER_PAGE)

  return default_render('tweets.html', kwargs)

@app.route('/articles', defaults={'page': 1})
@app.route("/articles/<int:page>")
def articles(page):
  return default_render('articles.html')

@app.route('/videos', defaults={'page': 1})
@app.route("/videos/<int:page>")
def videos(page):
  return default_render('videos.html')

@app.route("/ranking")
def ranking():
  return default_render('ranking.html')

if __name__ == "__main__":
  # postgres -D /usr/local/var/postgres
  # python app.py
  if settings.DEBUG:
    app.templates_auto_reload = True
    app.run(debug=True, use_reloader=True, use_debugger=True, host='0.0.0.0', port=8000)
  else:
    app.run()
