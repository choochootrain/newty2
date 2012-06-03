'''@short_description Scrapes website and stores the files in /scraped_news/website_name/files'''
'''@run sudo python get_html.py http://www.anywebsite.com/'''
'''@description downloads an entire website and does not force anything into the queue... that is yet to be implemented
   does a breadth first search starting from the home page. queue, errors, rejected, explored, visited lists are all stored in a text file
   catching kill signal is handled so feel free to kill the process as much as you want'''
import urllib2
import re
import os
import sys
import time
import random
import traceback
from download_package import *
from catch_kill import BreakHandler


'''This should be set true in the case of debug mode. If printing is true this will print to command line or else it prints into the log'''
printing = True


'''Initialize all the global variables necessary to run the code. In particular, this function builds the queue,
the explored set, the visited set and the rejected set'''
def initialize_globals():
    global url_to_scrape, url_short, queue_file_name
    global visited_file_name, rejected_file_name, errors_file_name
    global explored_file_name, queue, visited, rejected, errors, explored
    global write_visited, write_rejected, write_errors, write_explored, main_path

    main_path = '/scraped_news/'

    url_to_scrape = sys.argv[1]
    url_short = url_to_scrape.replace('http://', '').replace('www.', '').replace('/', '')
    

    queue_file_name = main_path + url_short + '/queue'
    visited_file_name = main_path + url_short + '/visited'
    rejected_file_name = main_path + url_short + '/rejected'
    errors_file_name = main_path + url_short + '/errors'
    explored_file_name = main_path + url_short + '/explored'

    queue = parse_file_by_line(queue_file_name)
    #visited = parse_file_by_line(visited_file_name)
    ensure_path(visited_file_name)
    #rejected = parse_file_by_line(rejected_file_name)
    ensure_path(rejected_file_name)
    #errors = parse_file_by_line(errors_file_name)
    ensure_path(errors_file_name)
    explored = parse_file_by_line(explored_file_name)


    
    #Need this or else runs into MemoryError on smaller servers
    #visited = set(visited)
    #rejected = set(rejected)
    #errors = set(errors)
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
    global write_visited, write_rejected, write_errors, write_explored
    write_to_queue()
    write_one(visited_file_name, write_visited)
    write_one(rejected_file_name, write_rejected)
    write_one(errors_file_name, write_errors)
    write_one(explored_file_name, write_explored)
    write_visited = ''
    write_rejected = ''
    write_errors = ''
    write_explored = ''

def write_one(file_name, text_to_write):
    f = open(file_name, 'a')
    f.write(text_to_write)
    f.close()

def write_to_queue():
    to_write = ''
    for x in queue:
        to_write += x.strip() + '\n'
    f = open(queue_file_name, 'w')
    f.write(to_write)
    f.close()


def begin_scrape():    
    global url_to_scrape, url_short, queue_file_name
    global visited_file_name, rejected_file_name, errors_file_name
    global explored_file_name, queue, visited, rejected, errors, explored
    global write_visited, write_rejected, write_errors, write_explored, main_path

    break_handler = BreakHandler()
    break_handler.enable()
    counter = 0
    file_parent_path = main_path + url_short + '/files/'
    log = open(main_path + url_short + '/log', 'a')
    while len(queue) > 0:
        if break_handler.trapped:
            break_handler.disable()
            write_everything()
            if printing:
                print 'Safely exited'
            log.write('Safely exited \n')
            log.close()
            sys.exit(1)
        counter += 1
        if counter > 100:
            log.close()
            log = open(main_path + url_short + '/log', 'a')
            write_everything()
            counter = 0
        current_url = queue.pop(0)
        if reject(current_url):
            write_rejected += current_url + '\n'
            continue
        random_wait = random.randint(0, 40) / 30.0
        time.sleep(.5 + random_wait)
        if printing:
            print 'Working on ' + current_url
        log.write('Working on ' + current_url + '\n')
        try:
            html = download_and_write_page(current_url, file_parent_path)
            links = [x.group(1) for x in re.finditer(r'href="([^"]*)"', html)]
            for new_url in links:
                new_url = new_url.strip()
                if new_url in explored:
                    continue
                if reject(new_url):
                    write_rejected += new_url + '\n'
##################################DO we want some way to store explored just in case we want to use those later? ###############################
                    #explored.add(new_url)
                    #write_explored += new_url + '\n'
                    continue
                else:
                    queue.append(new_url)
                    write_explored += new_url + '\n'
                    explored.add(new_url)
            #visited.add(current_url)
            write_visited += current_url + '\n'
        except:
            if printing:
                print 'error here'
                traceback.print_exc()
            log.write(traceback.format_exc())
            write_errors += current_url + '\n'



"""Not yet implemented. Currently does nothing, but if you want to put special seeds into your code run this"""
def queue_special():
    global queue, explored
    to_queue = []
    for x in to_queue:
        if x not in explored:
            queue.append(x)



if __name__ == '__main__':
    initialize_globals()
    if len(queue) == 0:
        queue.append(url_to_scrape)
    queue_special()
    begin_scrape()
    
