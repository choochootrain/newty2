#from pymongo import Connection
import re
import sys
import os
from useful_functions import *
import codecs
import traceback
import time
from application1.models import NewsSource, Article, BodyIndex, TitleIndex, ErrorsParsing
from datetime import datetime
exec('from ' + 'techcrunch.com'.replace('.com', '') + '_handler import *')

def usage():
    print 'Takes one command line argument: website name in the exact format of something like this http://www.nytimes.com with no slash in the end. Make sure there is a handler for\
your website. E.g. nytimes_handler.py for http://www.nytimes.com. MAKE SURE YOU CHANGE THE EXEC AT THE BEGINNING'

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
                new_error = ErrorsParsing(file_path = file_path)
                new_error.save()
                #errors.insert({'url' : url, 'file_path' : file_path})
                counter_failed += 1
                print str(counter_failed) + ' failed'
                continue
#print '***************** FAILURE *********************', file_path

            new_article = Article(url = url, file_path = file_path, title = data['title'].encode('utf8'), body = remove_tags(data['body']).encode('utf8'), date = data['date'], news_source = news_source)
            new_article.save()
            counter_succeeded += 1
            print str(counter_succeeded) + ' succeeded'
        except:
            new_error = ErrorsParsing(file_path = file_path)
            new_error.save()
            counter_failed += 1
            print str(counter_failed) + ' failed'
            traceback.print_exc()

                    

'''
def get_title(html):
    return 'title'

def get_body(html):
    return 'body'

def get_date(html):
    return 'date'
   ''' 

def main(full_website_name0):
    global full_website_name, website_name, db_name, news_source
    full_website_name = full_website_name0
    usage()
    x = raw_input('Type "yes" if you understand usage')
    if x != 'yes':
        sys.exit(1)
    if len(sys.argv) == 2:
        sys.argv[1] = full_website_name
    else:
        sys.argv.append(full_website_name)
    website_name = full_website_name.replace('http://', '').replace('www.', '')
    db_name = full_website_name.replace('http://', '').replace('www.', '')


    if len(NewsSource.objects.filter(name = db_name)) == 0:
        new_news_source = NewsSource(name = db_name)
        new_news_source.save()
        news_source = new_news_source
    else:
        news_source = NewsSource.objects.filter(name = db_name)[0]


    all_files = get_files('/scraped_news/' + website_name + '/files')
    all_paths_and_urls = get_paths_and_urls(all_files)
    write_to_database(all_paths_and_urls)


if __name__ == '__main__':
    global website_name, db_name, news_source
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    usage()
    full_website_name = sys.argv[1]
    website_name = full_website_name.replace('http://', '').replace('www.', '')
    exec('from ' + website_name.replace('.com', '') + '_handler import *')

    x = raw_input('Type "yes" if you understand usage')
    if x != 'yes':
        sys.exit(1)
    website_name = full_website_name.replace('http://', '').replace('www.', '')
    db_name = full_website_name.replace('http://', '').replace('www.', '')

    if len(NewsSource.objects.filter(name = db_name)) == 0:
        new_news_source = NewsSource(name = db_name)
        new_news_source.save()
        news_source = new_news_source
    else:
        news_source = NewsSource.objects.filter(name = db_name)[0]



    all_files = get_files('/scraped_news/' + website_name + '/files')
    all_paths_and_urls = get_paths_and_urls(all_files)
    write_to_database(all_paths_and_urls)
