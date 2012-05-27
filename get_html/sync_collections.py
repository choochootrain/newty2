from pymongo import Connection

"""techcrunch db is com db"""
c = Connection('localhost', 27018)
db = c[sys.argv[1]]

visited = db['visited']
queue = db['queue']
explored = db['explored']

queue.ensure_index('url')
explored.ensure_index('url')
visited.ensure_index('url')


for x in visited.find():
    url = x['url']
    if queue.find({'url' : url}).count > 0:
        for to_remove in queue.find({'url' : url}):
            queue.remove(to_remove)
    if explored.find({'url' : url}).count == 0:
        explored.insert({'url' : url})
    
