import sys
from multiprocessing import Pool
from process_template import *
from pymongo import Connection, ASCENDING, DESCENDING

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


def main():
    map_incremental(function_on_file, file_queue)
    sort_info_lambda = lambda queue_obj : sort_information(queue_obj, get_title, get_body,
                                            get_date, testing, success, failure, queue)
    map_incremental(sort_info_lambda, file_queue)


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
    if len(html_array) < 2:
        print 'failure'
        return
    body = html_array[1]
    clean_body = remove_tags(body)
    print clean_body
def get_date(html):
    print 'get date not yet implemented'
    

if __name__ == '__main__':
    main()


    
