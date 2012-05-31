import sys
from pymongo import Connection, ASCENDING, DESCENDING
import re
import HTMLParser
from datetime import datetime
import traceback
import time
"""Settings to edit"""
"""just prints stuff out and doesn't let you actually write to database"""
testing = True
connection = Connection('localhost', 27018)
iphone_example = connection['iphone_example']
iphone_articles = iphone_example['iphone_articles']
visited_articles = iphone_example['visited_articles']

article_database = connection['techcrunch_data']
all_articles = article_database['success']
"""all_articles has path, title, date, body"""


count = 0
for article in all_articles.find():
    if visited_articles.find({'path' : article['path']}) > 0:
        print 'already visited'
        continue
    count += 1
    if count > 100:
        count = 0
        visited_articles.ensure_index('path')
        print 'quit here'
        time.sleep(3)
        print 'cant quit now'
        
    visited_articles.insert({'path' : article['path']})
    if 'IPHONE' in article['title'].upper() and article['body'].upper().count('IPHONE') > 4:
        iphone_articles.insert({'path' : article['path'], 'title' : article['title'],
                                'date' : article['date'], 'body' : article['body']})
    if article['body'].upper().count('IPHONE') > 7:
        iphone_articles.insert({'path' : article['path'], 'title' : article['title'],
                                'date' : article['date'], 'body' : article['body']})
