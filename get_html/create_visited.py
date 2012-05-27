from pymongo import Connection
import sys

"""techcrunch is com"""
c = Connection('localhost', 27018)
db = c[sys.argv[1]]
get_input = raw_input('Are you sure you want to proceed? This will drop the visited collection. type YESCONTINUE to continue.')
if get_input == 'YESCONTINUE':
    db.drop_collection('visited')
else:
    sys.exit(0)
visited = db['visited']

queue = db['queue']
explored = db['explored']
queue.ensure_index('url')
explored.ensure_index('url')
visited.ensure_index('url')
to_insert = []
for x in explored.find():
    url = x['url']
    if queue.find({'url' : url}).count() == 0 and visited.find({'url' : url}).count() == 0:
        to_insert.append({'url' : url})


for x in to_insert:
    visited.insert(x)
