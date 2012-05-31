from pymongo import Connection
import sys

"""techcrunch is com"""
c = Connection('localhost', 27018)
db = c[sys.argv[1]]
get_input = raw_input('Are you sure you want to proceed? This will drop the visited collection. type YESCONTINUE to continue.')
if get_input == 'YESCONTINUE':
    print 'there is nothing here'
    sys.exit(0)
else:
    sys.exit(0)
visited = db['visited']

queue = db['queue']
explored = db['explored']
queue.ensure_index('url')
explored.ensure_index('url')
visited.ensure_index('url')


