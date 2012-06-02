import urllib2
import re
import os
import sys
import time
import random
import traceback
from download_package import *
from catch_kill import BreakHandler

'''downloads an entire website and does not force anything into the queue... that is yet to be implemented
   does a breadth first search starting from the home page. queue, errors, rejected, explored, visited lists are all stored in a text file
   catching kill signal is handled so feel free to kill the process as much as you want'''

'''to run: python get_html.py http://www.anywebsite.com/'''



def initialize_globals():
    global url_to_scrape, url_short, queue_file_name
    global visited_file_name, rejected_file_name, errors_file_name
    global explored_file_name, queue, visited, rejected, errors, explored
    global write_visited, write_rejected, write_errors, write_explored

    url_to_scrape = sys.argv[1]
    url_short = url_to_scrape.replace('http://', '').replace('www.', '').replace('/', '')
    

    queue_file_name = url_short + '/queue'
    visited_file_name = url_short + '/visited'
    rejected_file_name = url_short + '/rejected'
    errors_file_name = url_short + '/errors'
    explored_file_name = url_short + '/explored'

    queue = parse_file_by_line(queue_file_name)
    visited = parse_file_by_line(visited_file_name)
    rejected = parse_file_by_line(rejected_file_name)
    errors = parse_file_by_line(errors_file_name)
    explored = parse_file_by_line(explored_file_name)


    
    #Need this or else runs into MemoryError on smaller servers
    visited = set(visited)
    rejected = set(rejected)
    errors = set(errors)
    explored = set(explored)

    write_visited = ''
    write_rejected = ''
    write_errors = ''
    write_explored = ''

"""Define when to reject a url here"""
def reject(url):
    if url_short not in url:
        return True
    return False

def write_everything():
    write_to_queue()
    write_one(visited_file_name, write_visited)
    write_one(rejected_file_name, write_rejected)
    write_one(errors_file_name, write_errors)
    write_one(explored_file_name, write_explored)

def write_one(file_name, text_to_write):
    f = open(file_name, 'a')
    f.write(text_to_write)
    text_to_write = ''
    f.close()

def write_to_queue():
    to_write = ''
    for x in queue:
        to_write += x + '\n'
    f = open(queue_file_name, 'w')
    f.write(to_write)
    f.close()


def begin_scrape():    
    global url_to_scrape, url_short, queue_file_name
    global visited_file_name, rejected_file_name, errors_file_name
    global explored_file_name, queue, visited, rejected, errors, explored
    global write_visited, write_rejected, write_errors, write_explored

    break_handler = BreakHandler()
    break_handler.enable()
    counter = 0
    file_parent_path = url_short + '/files/'
    while len(queue) > 0:
        if break_handler.trapped:
            break_handler.disable()
            write_everything()
            print 'Safely exited'
            sys.exit(1)
        counter += 1
        if counter > 100:
            write_everything()
            counter = 0
        current_url = queue.pop(0)
        if reject(current_url):
            write_rejected += current_url + '\n'
            continue
        random_wait = random.randint(0, 40) / 30.0
        time.sleep(.5 + random_wait)
        print 'Working on ' + current_url
        try:
            html = download_and_write_page(current_url, file_parent_path)
            links = [x.group(1) for x in re.finditer(r'href="([^"]*)"', html)]
            for new_url in links:
                if new_url in explored:
                    continue
                if reject(new_url):
                    write_rejected += new_url + '\n'
                    explored.add(new_url)
                    write_explored += new_url + '\n'
                    continue
                else:
                    queue.append(new_url)
                    write_explored += new_url + '\n'
                    explored.add(new_url)
            visited.add(current_url)
            write_visited += current_url + '\n'
        except:
            print 'error here'
            traceback.print_exc()
            write_errors += current_url + '\n'






if __name__ == '__main__':
    initialize_globals()
    if len(queue) == 0:
        queue.append(url_to_scrape)
    begin_scrape()
    
