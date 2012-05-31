from pymongo import Connection
import sys


"""techcrunch db is com db"""
c = Connection('localhost', 27018)
db = c[sys.argv[1]]

visited = db['visited']
queue = db['queue']
explored = db['explored']

queue.ensure_index('url')
explored.ensure_index('url')
visited.ensure_index('url')



counter = 0

for x in explored.find():
    url = x['url']
    if queue.find({'url' : url}).count() == 0 and visited.find({'url' : url}).count() == 0:
        visited.insert({'url' : url})
        counter += 1

print counter



for x in visited.find():
    url = x['url']
    if queue.find({'url' : url}).count > 0:
        for to_remove in queue.find({'url' : url}):
            print 'going to remove something. shouldnt remove'
            #queue.remove(to_remove)
    if explored.find({'url' : url}).count == 0:
        print 'going to insert something. shouldnt insert'
        #explored.insert({'url' : url})
    
