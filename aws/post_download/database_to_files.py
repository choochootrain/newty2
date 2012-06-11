from pymongo import Connection
import re
import sys
import os
from useful_functions import *
import codecs
import traceback
import time



website_name = sys.argv[1].replace('http://', '').replace('www.', '')



counter = 0
c = Connection('localhost', 27018)
db = c['all_articles']
db_name = sys.argv[1].replace('http://', '').replace('www', '')
successes = db[db_name]
def database_to_files(website_name):
    for article in successes.find():
        to_write = str(article)
        f = open('/scraped_news/' + db_name + '/extracted/' + str(counter), 'w')
        f.write(to_write)
        f.close()
        counter += 1



if __name__ == '__main__':
    database_to_files(website_name)
