import urllib2
import re
import os
import sys
import time
import random
import traceback
from download_package import *
from catch_kill import BreakHandler



def initialize_globals():
    global url_to_scrape, url_short, queue_file_name
    global visited_file_name, rejected_file_name, errors_file_name
    global explored_file_name, queue, visited, rejected, errors, explored
    global write_visited, write_rejected, write_errors, write_explored

    url_to_scrape = sys.argv[1]
    url_short = url_to_scrape.replace('http://', '').replace('www', '')
    

    '''total explored is queue + visited'''
    queue_file_name = 'queue'
    visited_file_name = 'visited'
    rejected_file_name = 'rejected'
    errors_file_name = 'errors'
    explored_file_name = 'explored'


    queue = parse_file_by_line(queue_file_name)
    visited = set(parse_file_by_line(visited_file_name))
    rejected = set(parse_file_by_line(rejected_file_name))
    errors = set(parse_file_by_line(errors_file_name))
    explored = set(parse_file_by_line(explored_file_name))

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
            html = download_and_write_page(current_url)
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
    
