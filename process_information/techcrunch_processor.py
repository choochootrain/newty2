import sys
from multiprocessing import Pool
from process_template import *
from pymongo import Connection, ASCENDING, DESCENDING
import re
import HTMLParser
"""Settings to edit"""
"""just prints stuff out and doesn't let you actually write to database"""
testing = True
database_name = 'techcrunch_data'


connection = Connection('localhost', 27018)
"""EDIT THE DATABASE NAME"""
db = connection[database_name]
success = db['success']
failure = db['failure']
queue = db['queue']
explored = db['explored']
"""success has path, title, date, body"""
"""failure,queue, explored has path"""


"""@param main_dir is the directory where all the files are"""
main_dir = sys.argv[1]


"""queue of files to be called upon for one function. If you have 
multiple functions calling upon this create multiple queues"""
file_queue = get_queue(main_dir, explored, queue)


h = HTMLParser.HTMLParser()
def main():
    map_incremental(function_on_file, file_queue)
    sort_info_lambda = lambda queue_obj : find_basic_information(queue_obj, get_title, get_body,
                                            get_date, testing, success, failure, queue)
    map_incremental(sort_info_lambda, file_queue)


def function_on_file(queue_obj):
    file_path = queue_obj['path']
    f = open(file_path, 'r')
    html = f.read()
    f.close()
    print file_path


def get_title(html):
    title_begin = html.find('<title>')
    title_end = html[title_begin :].find('</title>')
    if title_begin == -1 or title_end == -1:
        print 'failure'
        return False
    """fix offsets"""
    title_end += title_begin
    title_begin += 7

    title = html[title_begin : title_end]
    print title
    return title
    
def get_body(html):
    a = html.find('<div class="body-copy">')
    html1 = html[a + 23 :]
    html_array = html1.split('</div>')
    if len(html_array) < 2:
        print 'failure'
        return False
    body = html_array[1]
    'scripts in the body'
    if body.find('<script>') != -1 or body.find('</script>') != -1:
        print 'failure'
        return False
    clean_body = remove_tags(body).strip().replace('\n', ' ')
    clean_body = re.sub(r'\s+', ' ', clean_body)
    clean_body = h.unescape(clean_body)

    print clean_body
    return clean_body
def get_date(html):
    length = len('<div class="post-time">')
    date_begin = html.find('<div class="post-time">')
    date_end = html[date_begin:].find('</div>')
    if date_begin == -1 or date_end == -1:
        print 'failure'
        return False
    date_end += date_begin
    date_begin += length

    date = html[date_begin : date_end]
    print date
    return date

if __name__ == '__main__':
    main()


    
