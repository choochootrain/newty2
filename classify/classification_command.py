import os
from pymongo import Connection, ASCENDING, DESCENDING
import re
import sys
'''@usage python classification_command.py http://www.anewssitehere'''
''' figure out a good news site to classify --- or possibly make it a completely different set
from the actual and in a different directory'''


news_site = sys.argv[1].replace('http://', '').replace('www', '')
#news_site = sys.argv[1]

connection = Connection('localhost', 27018)

db = connection['classification']
coll = db['all_stuff']
counter = int(sys.argv[3])

def training_phase():
    to_write = {}

    current_article_array = []
    while(counter > 0):
        current_article_obj = '' --- grab the first one that is not classified
        admin_input = ''
        while True:
            admin_input = raw_input('Classify this article. Type "Done" to finish this article. Type "Exit" to exit training. \n')
            if admin_input == 'Done':
                print '\n Finished this article \n\n\n'
                counter -= 1
                
            break
        if admin_input == 'Break':
            



def usage():
    print 'This command takes 3 arguments. The news site to use,  the full path to look into, and the count of news sites you want to classify'''


if __name__ == '__main__':
    training_phase()
