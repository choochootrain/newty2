import urllib2
from pymongo import Connection, ASCENDING, DESCENDING
import re
from Queue import Queue
import os
import sys
import time
import random
import traceback
from multiprocessing import Pool


""" from pymongo import Connection
c = Connection('localhost', 27018)
db = c['wsj']
db.drop_collection('explored')
db.drop_collection('queue')"""






begin_tags = r'<(div|td|tr|th|table|a|body|area|form|font|h1|h2|h3|h4|h5|h6|head|title|li|p|center|html|input|option|select|textarea|ul|i|b|label|footer|span)(>|[\s][^>^<^]*>)'
end_tags = r'</(div|td|tr|th|table|a|body|area|form|font|h1|h2|h3|h4|h5|h6|head|title|li|p|center|html|input|option|select|textarea|ul|i|b|label|footer|span)(>|[\s][^>^<^]*>)'
tags_regex = '<[^<^>]*>'

"""Filters out the files that have already been explored"""
def get_queue(main_dir, explored, queue):
    files_list = get_files(main_dir)
    for x in files_list:
        if explored.find({'path' : x}).count() == 0:
            entry = {'path' : x}
            explored.insert(entry)
            queue.insert(entry)
    file_queue = []
    print explored.count(), queue.count()
    for x in queue.find():
        file_queue.append(x)
    return file_queue


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


def map_files(function, file_queue):
    pool = Pool(processes=5)
    pool.map(function, file_queue)
    #for x in file_queue:
    #function(x)




def sort_information(queue_obj, get_title, get_body, get_date,
                     testing, success, failure, queue):
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
            failure.insert({'path' : file_path})
        traceback.print_exc()
    print file_path
    if not testing:
        queue.remove(queue_obj)

def remove_tags(html):
    tags = [(x.start(), x.end()) for x in re.finditer(tags_regex, html)]
    clean_html = ''
    prev_end = 0
    for begin, end in tags:
        clean_html += html[prev_end : begin]
        prev_end = end
    clean_html += html[prev_end : ]
    return clean_html




def to_bytestring (self, s, enc='utf-8'):
    """Convert the given unicode string to a bytestring, using the standard encoding,                                                                                                                     
    unless it's already a bytestring"""
    if s:
        if isinstance(s, str):
            return s
        else:
            return s.encode(enc)


