import os
import math

DEBUG = os.environ.get('EVEKATSU_DEBUG', 'false').lower() == 'true'

VERSION = '2'

DEADLINE_DAYS = int(os.environ.get('DEADLINE_DAYS', 100))

TWEETS_PER_PAGE = int(os.environ.get('TWEETS_PER_PAGE', 30))
USERS_PER_PAGE = int(os.environ.get('USERS_PER_PAGE', 30))

TWEETS_MAXIMUM_LIMIT = int(os.environ.get('TWEETS_MAXIMUM_LIMIT', 6000))

DEFAULT_CATEGORY = 'misc'
DEFAULT_SEARCH_QUERY = '%20exclude%3Aretweets&src=typd&lang=ja&count=100'
DEFAULT_MISC_QUERY = os.environ.get('DEFAULT_MISC_QUERY', 'q=eveonline%20OR%20"eve online"' + DEFAULT_SEARCH_QUERY)
SEARCH_QUERIES = [
    # (category, query, exclude_keyword, only_included_ids)
    ('evejapan', 'q=%23evejapan' + DEFAULT_SEARCH_QUERY,  None, False),
    ('eveonline', 'q=%23eveonline' + DEFAULT_SEARCH_QUERY, None, False),
    (DEFAULT_CATEGORY, DEFAULT_MISC_QUERY, r'eve ?online', False),
    (DEFAULT_CATEGORY, 'q=eve' + DEFAULT_SEARCH_QUERY, r'eve', True),
    (DEFAULT_CATEGORY, 'q=イブ' + DEFAULT_SEARCH_QUERY, None, True),
    (DEFAULT_CATEGORY, 'q=イヴ' + DEFAULT_SEARCH_QUERY, None, True),
    (DEFAULT_CATEGORY, 'q=いぶ' + DEFAULT_SEARCH_QUERY, None, True),
    (DEFAULT_CATEGORY, 'q="イブオンライン"' + DEFAULT_SEARCH_QUERY, None, True),
    (DEFAULT_CATEGORY, 'q="イヴオンライン"' + DEFAULT_SEARCH_QUERY, None, True),
    (DEFAULT_CATEGORY, 'q="いぶおんらいん"' + DEFAULT_SEARCH_QUERY, None, True),
]
