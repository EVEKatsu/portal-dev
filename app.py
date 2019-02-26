from datetime import datetime
import re

from flask import Flask, render_template
from flask_sqlalchemy import Pagination

import settings
from initialize import app, db
from models import Tweet

URL_PATTERN = r'https?:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+'

def default_kwargs():
  return {
    'SITENAME': 'イブカツ！',
    'SITEURL': 'https://evekatsu.herokuapp.com',
    'DATETIME': datetime.now(),
    'MENUITEMS': (
        ('ツイッター', 'tweets'),
        ('ブログ', 'feeds'),
        ('動画', 'videos'),
        ('ランキング', 'ranking'),
    )
  }

def default_render(template_name_or_list, kwargs={}):
  return render_template(template_name_or_list, **{**default_kwargs(), **kwargs})

@app.route("/")
def index():
  return default_render('index.html')

@app.route('/tweets', defaults={'category': 'all', 'page': 1})
@app.route("/tweets/<string:category>/<int:page>")
def tweets(category, page):
  kwargs = {
    'category': category,
    'TWEETS_MENUITEMS': (
      ('すべて', 'all'),
      ('#evejapan', 'evejapan'),
      ('#eveonline', 'eveonline'),
      ('その他', 'misc'),
    )
  }

  if category == 'all':
    query = Tweet.query
  else:
    query = Tweet.query.filter(Tweet.category == category)

  # tweets = Tweet.query.order_by(Tweet.created_at.desc()).paginate(page, DEFAULT_PAGINATION)
  # for tweet in tweets.items:
  #   for url in re.findall(URL_PATTERN, tweet.text):
  #     print(url)
  #     tweet.text = tweet.text.replace(
  #       url,
  #       '<a href="' + url + '" target="_blank">[外部リンク]</a>'
  #     )

  kwargs['tweets'] = query.order_by(Tweet.created_at.desc()).paginate(page, settings.DEFAULT_PAGINATION)

  return default_render('tweets.html', kwargs)

@app.route('/feeds', defaults={'page': 1})
@app.route("/feeds/<int:page>")
def feeds(page):
  return default_render('feeds.html')

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
    print('hoge')
    app.templates_auto_reload = True
    app.run(debug=True, use_reloader=True, use_debugger=True, host='0.0.0.0', port=8000)
  else:
    app.run()
