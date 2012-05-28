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
forced_queue = db['forced_queue']
errors = db['errors']
visited = db['visited']

"""Key variables to use:
queue
explored
errors"""

def list_of_dates():
    months_and_days = ((1, 31), (2, 29), (3, 31), (4, 30), (5, 31), (6, 30),
                       (7, 31), (8, 31), (9, 30), (10, 31), (11, 30), (12, 31))
    #years = (2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012)
    years = (2006, 2007, 2008, 2009, 2010, 2011, 2012)
    formatted_dates = []
    for year in years:
        for month, days in months_and_days:
            for day in range(1, days + 1):
                if year%4 != 0 and month == 2 and day == 29:
                    continue
                if year == 2012 and month >= 6:
                    continue
                year_str = str(year)
                month_str = str(month)
                day_str = str(day)
                if len(day_str) == 1:
                    day_str = '0' + day_str
                if len(month_str) == 1:
                    month_str = '0' + month_str
                formatted_dates.append('/' + year_str + '/' + month_str + '/' + day_str + '/')
    return formatted_dates



def force_queue_urls():
    to_force = []
    list_dates = list_of_dates()
    for x in list_dates:
        to_force.append('http://techcrunch.com' + x)
        print x
    return to_force

def main():
    get_input = raw_input('This assumes you have created a visited collection \n type yes if you have already created \n')
    if get_input != 'yes':
        return



    global forced_queue_cursor
    """This is the section put into the forced queue"""
    if forced_queue.count() == 0:
        entries_to_force = force_queue_urls()
        for x in entries_to_force:
            forced_queue.insert({'url' : x})
            print x
        forced_queue_cursor = forced_queue.find()
        begin_scrape()
    else:
        forced_queue_cursor = forced_queue.find()
        begin_scrape()

"""ORIGINALLY THIS ACCIDENTALLY REJECTED anythin with month october 10"""
date_match = re.compile('.*20[0-1][0-9]/[0-1][0-9]/[0-3][0-9].*')
def reject_url(url):
    if visited.find({'url' : url}).count() != 0:
        return True
    if not date_match.match(url):
        print 'rejected ' + url
        return True
    return False
def begin_scrape():
    while forced_queue_cursor.count():
        forced_queue.ensure_index('url')
        visited.ensure_index('url')

        current_url_obj = forced_queue_cursor[0]
        current_url = current_url_obj['url']
        if reject_url(current_url):
            forced_queue.remove(current_url_obj)
            continue

        random_wait = random.randint(0, 70) / 30.0
        time.sleep(wait_time + random_wait)

        forced_queue.remove(current_url_obj)

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

            for x in links:
                if url_short in x and visited.find({'url' : x}).count() == 0 and forced_queue.find({'url' : x}).count() == 0:
                    forced_queue.insert({'url' : x})
            
            visited.insert({'url' : current_url})
        except:
            print 'error here'
            traceback.print_exc()
            errors.insert({'url' : current_url})
        """TO BEGIN HERE TOMORROW. x not in explored_set --> explored.find("""





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
