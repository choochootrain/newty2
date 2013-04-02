from pymongo import Connection
import re
import sys
import os
from useful_functions import *
import codecs
import traceback
import time
import chardet
website_name = sys.argv[1].replace('http://', '').replace('www.', '')
exec('from ' + website_name.replace('.com', '') + '_handler import *')

def usage():
    print 'Takes one command line argument: website name in the exact format of something like this http://www.nytimes.com with no slash in the end'
    print 'Testing command: Takes two command line arguments: website name and then a url to use that websites parser to test. e.g. python write_to_database.py http://www.nytimes.com http://www.nytimes.com/an_article_here'

"""current dir begins with main_dir as current_dir and is recursive and finds all file paths in the main_dir"""
def get_files(current_dir):
    files_list = []
    files = os.listdir(current_dir)
    for file in files:
        file_path = current_dir + '/' + file
        if os.path.isdir(file_path):
            files_list.extend(get_files(file_path))
        else:
            files_list.append(file_path)
    return files_list


def get_paths_and_urls(all_file_paths):
    all_paths_and_urls = []
    for file_path in all_file_paths:
        url = 'http://' + file_path.replace('/scraped_news/' + website_name + '/files/', '')[:-5]
        #print url
        all_paths_and_urls.append((file_path, url))
    return all_paths_and_urls


#mongod --port 27018
c = Connection('localhost', 27018)
db = c['all_articles']
coll = db[sys.argv[1].replace('http://', '').replace('www.', '')]
error = db['error_' + sys.argv[1].replace('http://', '').replace('www.', '')]
def write_to_database(all_paths_and_urls):
    counter_failed = 0
    counter_succeeded = 0
    for file_path, url in all_paths_and_urls:
        #time.sleep(.5)
        if reject(url):
            continue
        try:
            #f = open(file_path, 'r')
            f = codecs.open(file_path, 'r', 'iso-8859-1')
            html = f.read()
            f.close()
            data = find_basic_information(html, url, get_title, get_body, get_date)
            if data == False:
                counter_failed += 1
                print str(counter_failed) + ' failed'
                error.insert({'url' : url})
                continue

#print '***************** FAILURE *********************', file_path

            to_insert = {'url' : url, 'file_path' : file_path, 'title' : data['title'],
                         'body' : remove_tags(data['body']), 'date' : data['date']}
            print data['title'], data['date'], data['body'][:25], '\n\n\n'
            counter_succeeded += 1
            print str(counter_succeeded) + ' succeeded'
            coll.insert(to_insert)
        except:
            counter_failed += 1
            print str(counter_failed) + ' failed'
            traceback.print_exc()






'''TEST CODE'''
"""Handles opening sites that force you to redirect. """
class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
    http_error_301 = http_error_303 = http_error_307 = http_error_302

"""Url Parser : use as page = url_opener.open(url)"""
cookie_handler = urllib2.HTTPCookieProcessor()
url_opener = urllib2.build_opener(MyHTTPRedirectHandler, cookie_handler)
url_opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5')]

def to_bytestring (s, enc='utf-8'):
    """Convert the given unicode string to a bytestring, using the standard encoding,
    unless it's already a bytestring"""
    if s:
        if isinstance(s, str):
            return s
        else:
            return s.encode(enc)

def test(url):
    connection = url_opener.open(url)
    html = connection.read()
    #addressing http://stackoverflow.com/questions/4790078/python-htmlparser-unicodedecodeerror
    #encoding = connection.headers.getparam('charset')
    encoding = chardet.detect(html)['encoding']
    html = html.decode(encoding)
    print get_title(html, url)
    print get_date(html, url)
    print get_body(html, url)


'''
def get_title(html):
    return 'title'

def get_body(html):
    return 'body'

def get_date(html):
    return 'date'
   '''

if __name__ == '__main__':
    print 'REACHED'
    if len(sys.argv) == 3:
        test(sys.argv[2])
        sys.exit(1)
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    website_name = sys.argv[1].replace('http://', '').replace('www.', '')
    all_files = get_files('/scraped_news/' + website_name + '/files')
    all_paths_and_urls = get_paths_and_urls(all_files)
    write_to_database(all_paths_and_urls)
