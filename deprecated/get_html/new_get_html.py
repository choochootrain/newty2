import urllib2
from pymongo import Connection, ASCENDING, DESCENDING
import re
import os
import sys
import time
import random
import traceback

"""Handles opening sites that force you to redirect. """
class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
    http_error_301 = http_error_303 = http_error_307 = http_error_302



"""To do bulk insert entry = [{k:v}, {k:v}]
coll.insert(entry)
This inserts two entries
Minimize database queries/requests """


"""Key variables to use:
queue
explored
errors"""
def main():
    global queue_cursor
    if queue.count() == 0:
        new_entry = {'url' : url_to_scrape}
        queue.insert(new_entry)
        queue_cursor = queue.find()
        begin_scrape()
    else:
        queue_cursor = queue.find()
        begin_scrape()

"""define when to reject a url here"""
def reject(url):
    return False
def begin_scrape():
    while queue_cursor.count():
        queue.ensure_index('url')
        explored.ensure_index('url')

        current_url_obj = queue_cursor[0]
        current_url = current_url_obj['url']
        if reject(current_url):
            queue.remove(current_url_obj)
            continue
        random_wait = random.randint(0, 40) / 30.0
        time.sleep(wait_time + random_wait)
        queue.remove(current_url_obj)
        print 'Working on ' + current_url
        try:
            page = url_opener.open(current_url)
            html = page.read()
            if not url_short in current_url:
                continue
            url_no_http = current_url.replace('http://', '')
            account_for_last_slash = url_regex.search(url_no_http)
            if account_for_last_slash and account_for_last_slash.group(0) == url_no_http:
                url_no_http = account_for_last_slash.group(1)
            ensure_path(url_no_http)
            f = open(url_no_http + '_file', 'w')
            f.write(html)
            f.close()
            links = [x.group(1) for x in re.finditer(r'href="([^"]*)"', html)]

            add_explored = []
            add_queue = []
            add_explored_ele = []
            for x in links:
            #if url_short in x and x not in explored_set:
                if url_short in x and explored.find({'url' : x}).count() == 0 and x not in add_explored_ele:
                    add_explored.append({'url' : x})
                    add_explored_ele.append(x)
                    add_queue.append({'url' : x})
            if len(add_explored) > 0:
                explored.insert(add_explored)
                add_explored = []
            if len(add_queue) > 0:
                queue.insert(add_queue)
                add_queue = []
        except:
            print 'error here'
            traceback.print_exc()
            errors.insert({'url' : current_url})
        """TO BEGIN HERE TOMORROW. x not in explored_set --> explored.find("""



"""Variables"""
random_wait = True
wait_time = 1
url_to_scrape = sys.argv[1]
url_short = url_to_scrape.replace('http://', '').replace('www', '')
insert_interval = 100

"""MongoDB Variables"""
connection = Connection('localhost', 27018)
url_split = url_to_scrape.split('.')
db = connection[url_split[1]]
queue = db['queue']
explored = db['explored']
errors = db['errors']


"""Url Parser : use as page = url_opener.open(url)"""
cookie_handler = urllib2.HTTPCookieProcessor()
url_opener = urllib2.build_opener(MyHTTPRedirectHandler, cookie_handler)
url_opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5')]


"""Regex expressions"""
directory_regex = re.compile('(.*)/[^/]+')
url_regex = re.compile('(.*)/')
directories_exist = set()

"""Call this function on a url without http
to make sure a directory exists to save a file"""
def ensure_path(url):
    if '/' not in url:
        return
    path = directory_regex.search(url).group(1)
    if path in directories_exist:
        return
    if not os.path.exists(path):
        os.makedirs(path)
        directories_exist.add(path)


def to_bytestring (s, enc='utf-8'):
    """Convert the given unicode string to a bytestring, using the standard encoding,                                                                                                                     
    unless it's already a bytestring"""
    if s:
        if isinstance(s, str):
            return s
        else:
            return s.encode(enc)



if __name__ == '__main__':
    main()
