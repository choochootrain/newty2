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



class ProcessTemplate:
    @classmethod
    def __init__(cls, main_dir, news_name):
        cls.testing = True
        cls.main_dir = main_dir
        cls.connection = Connection('localhost', 27018)
        cls.db = cls.connection[news_name]
        cls.success = cls.db['success']
        cls.failure = cls.db['failure']
        cls.queue = cls.db['queue']
        cls.explored = cls.db['explored']
        cls.begin_tags = r'<(div|td|tr|th|table|a|body|area|form|font|h1|h2|h3|h4|h5|h6|head|title|li|p|center|html|input|option|select|textarea|ul|i|b|label|footer|span)(>|[\s][^>^<^]*>)'
        cls.end_tags = r'</(div|td|tr|th|table|a|body|area|form|font|h1|h2|h3|h4|h5|h6|head|title|li|p|center|html|input|option|select|textarea|ul|i|b|label|footer|span)(>|[\s][^>^<^]*>)'
        cls.tags_regex = '<[^<^>]*>'

        cls.file_queue = cls.get_queue()
        """success has path, title, date, body"""
        """failure has path"""

    @classmethod
    def get_queue(cls):
        files_list = cls.get_files(cls.main_dir)
        for x in files_list:
            if cls.explored.find({'path' : x}).count() == 0:
                entry = {'path' : x}
                cls.explored.insert(entry)
                cls.queue.insert(entry)
        queue_list = []
        print cls.explored.count(), cls.queue.count()
        for x in cls.queue.find():
            queue_list.append(x)
        return queue_list
        

    @classmethod
    def function_on_file(cls, queue_obj):
        cls.sort_information(queue_obj)
    @classmethod
    def get_title(cls, html):
        pass
    @classmethod
    def get_body(cls, html):
        pass
    @classmethod
    def get_date(cls, html):
        pass
    @classmethod
    def sort_information(cls, queue_obj):
        file_path = queue_obj['path']
        f = open(file_path, 'r')
        html = f.read()
        try:
            title = cls.get_title(html)
            body = cls.get_body(html)
            date = cls.get_date(html)
            f.close()
            entry = {'path' : file_path, 'title' : title, 'body' : body, 'date' : date}
            if not cls.testing:
                cls.success.insert(entry)
        except:
            if not cls.testing:
                cls.error.insert({'path' : file_path})
            traceback.print_exc()
        print file_path
        if not cls.testing:
            cls.queue.remove(queue_obj)

    """current dir begins with main_dir as current_dir and is recursive and finds all file paths in the main_dir"""
    @classmethod
    def get_files(cls, current_dir):
        files_list = []
        files = os.listdir(current_dir)
        for file in files:
            file_path = current_dir + '/' + file
            if os.path.isdir(file_path):
                files_list.extend(cls.get_files(file_path))
            else:
                files_list.append(file_path)
        return files_list

    @classmethod
    def remove_tags(cls, html):
        tags = [(x.start(), x.end()) for x in re.finditer(cls.tags_regex, html)]
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


