from pymongo import Connection
import re
import sys
import os
from useful_functions import *
import codecs
import traceback
import time
import json


website_name = sys.argv[1].replace('http://', '').replace('www.', '')



counter = 0
c = Connection('localhost', 27018)
db = c['all_articles']
db_name = sys.argv[1].replace('http://', '').replace('www.', '')
successes = db[db_name]
def database_to_files(website_name):
    global counter, db_name
    ensure_path('/scraped_news/' + db_name + '/extracted/0')
    for article in successes.find():
        body = article['body']
        title = article['title']
        _id = str(article['_id'])
        date = article['date'].strftime("%h %d, %Y")
        to_write = json.dumps({'body' : body, 'title' : title, '_id' : _id, 'date' : date})
        f = open('/scraped_news/' + db_name + '/extracted/' + str(counter), 'w')
        f.write(to_write)
        f.close()
        counter += 1

directory_regex = re.compile('(.*)/[^/]+')
'''If the path for the url exists, do nothing. If path does not exist, creates the path'''
def ensure_path(url_no_http):
    if '/' not in url_no_http:
        return
    path = directory_regex.search(url_no_http).group(1)
    if not os.path.exists(path):
        os.makedirs(path)



if __name__ == '__main__':
    database_to_files(website_name)
