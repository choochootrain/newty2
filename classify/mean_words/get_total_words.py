from pymongo import Connection
import re
c = Connection('localhost', 27018)
db = c['all_articles']
coll = db['techcrunch.com']

only_alphanumeric = re.compile('[\W_]+')
title_count = 0
body_count = 0
for article in coll.find():
    body_count += len(only_alphanumeric.sub(' ', article['body'].replace(u'\u00A0', ' ').lower()).split(' '))
    title_count += len(only_alphanumeric.sub(' ', article['title'].replace(u'\u00A0', ' ').lower()).split(' '))

print str(body_count) + ' number body words'
print str(title_count) + ' number title words'
