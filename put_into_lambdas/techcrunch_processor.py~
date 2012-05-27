import sys
from multiprocessing import Pool
from process_template import *
from pymongo import Connection, ASCENDING, DESCENDING

testing = True
connection = Connection('localhost', 27018)
db = connection['techcrunch_data']
success = db['success']
failure = db['failure']
queue = db['queue']
explored = db['explored']
"""success has path, title, date, body"""
"""failure,queue, explored has path"""


main_dir = sys.argv[1]
file_queue = get_queue(main_dir, explored, queue)


news_name = 'techcrunch_data'


def main():
    map_files(function_on_file, file_queue)
    x = lambda queue_obj : sort_information(queue_obj, get_title, get_body,
                                            get_date, testing, success, failure, queue)
    def hax0rs(a):
        return x(a)
    map_files(hax0rs, file_queue)


def function_on_file(queue_obj):
    file_path = queue_obj['path']
    f = open(file_path, 'r')
    html = f.read()
    f.close()
    print file_path


def get_title(html):
    print 'get title not yet implemented'
def get_body(html):
    print 'get body not yet implemented'
    a = html.find('<div class="body-copy">')
    html1 = html[a + 23 :]
    html_array = html1.split('</div>')
    body = html_array[0]
    clean_body = remove_tags(body)
    print clean_body
def get_date(html):
    print 'get date not yet implemented'
    

if __name__ == '__main__':
    main()


    
