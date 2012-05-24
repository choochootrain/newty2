import urllib2
from pymongo import Connection, ASCENDING, DESCENDING
import re
from Queue import Queue
import os
import sys
import time
import random
import traceback

testing = True


begin_tags = r'<(div|td|tr|th|table|a|body|area|form|font|h1|h2|h3|h4|h5|h6|head|title|li|p|center|html|input|option|select|textarea|ul|i|b|label|footer|span)(>|[\s][^>^<^]*>)'
end_tags = r'</(div|td|tr|th|table|a|body|area|form|font|h1|h2|h3|h4|h5|h6|head|title|li|p|center|html|input|option|select|textarea|ul|i|b|label|footer|span)(>|[\s][^>^<^]*>)'

tags_regex = '<[^<^>]*>'


"""Global setting variables"""
main_dir = sys.argv[1]

"""@toedit"""
news_name = 'techcrunch_data'
news_name = 'insert name here.'
#news_name = 'usatoday_data'
#news_name = 'techcrunch_data'
#news_name = 'wsj_data'
#news_name = 'nyt_data'


"""@toedit"""
def get_title(html):
    print 'get title not yet implemented'

"""@toedit"""
def get_body(html):
    print 'get body not yet implemented'
    a = html.find('<div class="body-copy">')
    html1 = html[a + 23 :]
    html_array = html1.split('</div>')
    body = html_array[1]
    clean_body = remove_tags(body)
    print clean_body


"""@toedit"""
def get_date(html):
    print 'get date not yet implemented'



def remove_tags(html):
    tags = [(x.start(), x.end()) for x in re.finditer(tags_regex, html)]
    clean_html = ''
    prev_end = 0
    for begin, end in tags:
        clean_html += html[prev_end : begin]
        prev_end = end
    clean_html += html[prev_end : ]
    return clean_html
    


connection = Connection('localhost', 27018)
db = connection[news_name]
success = db['success']
failure = db['failure']
queue = db['queue']
explored = db['explored']
"""success has path, title, date, body"""
"""failure has path"""



""" from pymongo import Connection
c = Connection('localhost', 27018)
db = c['wsj']
db.drop_collection('explored')
db.drop_collection('queue')"""


"""Define what to do with each file"""
from bs4 import BeautifulSoup
def function_on_file(queue_obj):
    file_path = queue_obj['path']
    f = open(file_path, 'r')
    html = f.read()
    try:
        title = get_title(html)
        body = get_body(html)
        date = get_date(html)
        f.close()
        entry = {'path' : file_path, 'title' : title, 'body' : body, 'date' : date}
        if not testing:
            success.insert(entry)
    except:
        if not testing:
            error.insert({'path' : file_path})
        traceback.print_exc()
    print file_path
    if not testing:
        queue.remove(queue_obj)

"""Do something on error collection and url_collection"""





"""current dir begins with main_dir as current_dir and is recursive and finds all file paths in the main_dir"""
def get_files(current_dir = main_dir):
    files_list = []
    files = os.listdir(current_dir)
    for file in files:
        file_path = current_dir + '/' + file
        if os.path.isdir(file_path):
            files_list.extend(get_files(file_path))
        else:
            files_list.append(file_path)
    return files_list

from multiprocessing import Pool
def main():
    set_up_globals()
    files_list = get_files(main_dir)
    for x in files_list:
        if explored.find({'path' : x}).count() == 0:
            entry = {'path' : x}
            explored.insert(entry)
            queue.insert(entry)
    queue_list = []
    print explored.count(), queue.count()
    for x in queue.find():
        queue_list.append(x)
    
    #for x in files_list:
        #print x
    #print '\n\n\n'
    pool = Pool(processes=5)
    pool.map(function_on_file, queue_list)

    
def set_up_globals():
    global connection, db, url_collection, error_collection
    connection = Connection('localhost', 27018)
    db = connection.process_html
    url_collection = db[news_name]
    error_collection = db[news_name + '_errors']
    


    


directories_exist = set()
directory_regex = re.compile('(.*)/[^/]+')
url_regex = re.compile('(.*)/')
def ensure_path(url):
    if '/' not in url:
        return
    path = directory_regex.search(url).group(1)
    if path in directories_exist:
        return
    if not os.path.exists(path):
        os.makedirs(path)
        directories_exist.add(path)


def begin_get(url_queue, explored_set, current_counter):
    save_counter = 0
    while not url_queue.empty():
        save_counter += 1
        if save_counter > backup_interval:
            current_counter = save_entry(explored_set, url_queue, current_counter)
            save_counter = 0
        url = url_queue.get()
        print 'Working on ' + url
        try :
            page = url_opener.open(url)
        except:
            error_entry = {'url' : url}
            error_collection.insert(error_entry)
            continue
        html = page.read()
        if not url_short in url:
            continue
        url = url.replace('http://', '')
        account_for_last_slash = url_regex.search(url)
        if account_for_last_slash and account_for_last_slash.group(0) == url:
            url = account_for_last_slash.group(1)
        ensure_path(url)

        try: 
            f = open(url + '_file', 'w')
            f.write(html)
            f.close()
        except:
            error_entry = {'url' : url, 'error' :  'cannot find path even though path ensured'}
            error_collection.insert(error_entry)
            continue
        random_wait = random.randint(0, 70)/30.0
        time.sleep(wait_time + random_wait)
        
        """Finds new urls"""
        links = [x.group(1) for x in re.finditer(r'href="([^"]*)"', html)]
        for x in links:
            if url_to_scrape in x and x not in explored_set:
                explored_set.add(x)
                url_queue.put(x)
        

    print 'finished'
    

    

def save_entry(explored_set, url_queue, counter):
    print "CURRENTLY SAVING POSITION. DO NOT QUIT"
    counter += 1
    explored_array = []
    for x in explored_set:
        explored_array.append(x)

    url_array = []
    while not url_queue.empty():
        url_array.append(url_queue.get())
    for x in url_array:
        url_queue.put(x)
        
    new_entry = {'counter' : counter, 'url_array' : url_array, 'explored_array' : explored_array}
    url_collection.insert(new_entry)
    print "CAN QUIT NOW"
    return counter


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
