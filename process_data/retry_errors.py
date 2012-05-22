import urllib2
from pymongo import Connection, ASCENDING, DESCENDING
import re
from Queue import Queue
import os
import sys
import time
import random


url_dict = {'techcrunch.com' : 'http://techcrunch.com', 'bbc.co.uk' : 'http://www.bbc.co.uk/', 'usatoday.com' : 'http://www.usatoday.com'}





def main():
    cookie_handler = urllib2.HTTPCookieProcessor()
    url_opener = urllib2.build_opener(MyHTTPRedirectHandler, cookie_handler)
    url_opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5')]

    techcrunch = []
    bbc = []
    usaToday = []
    
    url_to_list = {'techcrunch.com' : techcrunch, 'bbc.co.uk' : bbc, 'usatoday.com' : usaToday}
    
    connection = Connection('localhost', 27018)
    db = connection.get_html
    error_collection = db['errors']
    
    for x in error_collection.find({'error' : {'$exists' : False}}):
        for k, v in url_to_list.items():
            if k in x['url']:
                v.append(x)

    collection_techcrunch = db['http://techcrunch.com']
    collection_bbc = db['http://www.bbc.co.uk/']
    collection_usa = db['http://www.usatoday.com']    
    list_url = [(techcrunch, collection_techcrunch), (bbc, collection_bbc), (usaToday, collection_usa)]
    success = []

    for k, v in list_url:
        all_entries = v.find({'counter' : {'$exists' : True}}).sort('counter', DESCENDING)
        current_entry = all_entries[0]
        counter = current_entry['counter']
        current_queue = current_entry['url_array']
        explored_set = set(current_entry['explored_array'])
        for error in k:
            url = error['url']
            try:
                time.sleep(.2 + random.randint(0,30)/30.0)
                print 'working on ' + url
                page = url_opener.open(url)
                html = page.read()
                url = url.replace('http://', '')
                account_for_last_slash = url_regex.search(url)
                if account_for_last_slash and account_for_last_slash.group(0) == url:
                    url = account_for_last_slash.group(1)
                ensure_path(url)
                f = open(url + '_file', 'w')
                f.write(html)
                f.close()

                """Find new urls"""
                links = [x.group(1) for x in re.finditer(r'href="([^"]*)"', html)]
                for x in links:
                    if url_to_scrape in x and x not in explored_set:
                        explored_set.add(x)
                        current_queue.append(x)
                success.append(error)
            except:
                print 'failed'
        explored_array = []
        for x in explored_set:
            explored_array.append(x)
        new_entry = {'counter' : counter + 1, 'url_array' : current_queue, 'explored_array' : explored_array}
        v.insert(new_entry)
        
        for x in success:
            error_collection.remove(x)
    """Determines which urls to scrape through storing previous entries in database"""

directories_exist = set()
directory_regex = re.compile('(.*)/[^/]+')
url_regex = re.compile('(.*)/')

def to_bytestring (s, enc='utf-8'):
    """Convert the given unicode string to a bytestring, using the standard encoding,                                                                                                                     
    unless it's already a bytestring"""
    if s:
        if isinstance(s, str):
            return s
        else:
            return s.encode(enc)

"""Handles opening sites that force you to redirect. """
class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
    http_error_301 = http_error_303 = http_error_307 = http_error_302








if __name__ == '__main__':
    main()
