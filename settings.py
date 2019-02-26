import os

DEBUG = os.environ.get('EVEKATSU_DEBUG', 'false').lower() == 'true'

#DAMMY_TWITTER_ID = os.environ.get('DAMMY_TWITTER_ID', 'kx6txew2')

DEFAULT_PAGINATION = 50

DEFAULT_CATEGORY = 'misc'
DEFAULT_SEARCH_QUERY = '%20exclude%3Aretweets&src=typd&lang=ja&count=100'
SEARCH_QUERIES = [
    ('evejapan', '%23evejapan'),
    ('eveonline', '%23eveonline'),
    (DEFAULT_CATEGORY, '"eve%20online"%20eveonline%20-%40eveonline'),
]