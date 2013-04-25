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



def get_error_path_from_url(url):
    file_path = '/scrape_news/' + website_name.replace('http://', '') + '/files/' + url.replace('http://', '') + '_file'
    return file_path


#mongod --port 27018

def fix_errors():
    c = Connection('localhost', 27018)
    db = c['all_articles']
    coll = db[sys.argv[1].replace('http://', '').replace('www.', '')]
    errors = db['error_' + sys.argv[1].replace('http://', '').replace('www.', '')]
    file_paths_and_urls = []
    counter_failed = 0
    for error_entry in errors.find():
        url = error_entry['url']
        file_path = get_error_path_from_url(url)
        print file_path
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
                #error.insert({'url' : url, 'file_path' : file_path})
                #Don't insert again because it's already in the error
                continue

#print '***************** FAILURE *********************', file_path

            to_insert = {'url' : url, 'file_path' : file_path, 'title' : data['title'],
                         'body' : remove_tags(data['body']), 'date' : data['date']}
            print data['title'], data['date'], data['body'][:25], '\n\n\n'
            counter_succeeded += 1
            print str(counter_succeeded) + ' FIXED'
            coll.insert(to_insert)
            errors.remove({'url' : url})
        except:
            counter_failed += 1
            print str(counter_failed) + ' failed'
            traceback.print_exc()



if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    website_name = sys.argv[1].replace('http://', '').replace('www.', '')
    fix_errors()
