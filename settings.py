import os

DEBUG = os.environ.get('EVEKATSU_DEBUG', 'false').lower() == 'true'

VERSION = '4'

DEADLINE_DAYS = int(os.environ.get('DEADLINE_DAYS', 100))

TWEETS_PER_PAGE = int(os.environ.get('TWEETS_PER_PAGE', 30))
USERS_PER_PAGE = int(os.environ.get('USERS_PER_PAGE', 30))

TWEETS_MAXIMUM_LIMIT = int(os.environ.get('TWEETS_MAXIMUM_LIMIT', 6000))

DEFAULT_CATEGORY = 'misc'

DEFAULT_SEARCH_PARAMS = {
    'count': 100,
    'result_type': 'mixed',
    'include_entities': True,
}

DEFAULT_MISC_QUERY = os.environ.get('DEFAULT_MISC_QUERY', 'eveonline OR "eve online" lang:ja')
SEARCH_QUERIES = [
    # (category, search_words, exclude_keyword, only_included_ids)
    ('evejapan', '#evejapan',  None, False),
    ('eveonline', '#eveonline lang:ja', None, False),
    ('zkillboard', 'zkillboard.com lang:ja', None, False),
    (DEFAULT_CATEGORY, DEFAULT_MISC_QUERY, r'eve ?online', False),
    (DEFAULT_CATEGORY, 'eve lang:ja', r'eve', True),
    (DEFAULT_CATEGORY, 'イブ', None, True),
    (DEFAULT_CATEGORY, 'イヴ', None, True),
    (DEFAULT_CATEGORY, 'いぶ', None, True),
    (DEFAULT_CATEGORY, '"イブオンライン"', None, True),
    (DEFAULT_CATEGORY, '"イヴオンライン"', None, True),
    (DEFAULT_CATEGORY, '"いぶおんらいん"', None, True),
]
