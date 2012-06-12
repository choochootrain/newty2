from pymongo import Connection, DESCENDING, ASCENDING
import sys
import operator
import json
print 'columns are total_words, percentages, date, newspaper, word_count'

c = Connection('192.168.2.5', 27018)
db = c['words']
iphone = db[sys.argv[1]]


threshold = float(sys.argv[2])
counts_per_date = {}
for entry in iphone.find().sort('date', DESCENDING):
    date = entry['date']
    percentage = entry['percentage']
    if percentage > threshold:
        if date in counts_per_date:
            counts_per_date[date] += 1
        else:
            counts_per_date[date] = 1

s = False
g = 0
sorted_counts = sorted(counts_per_date.iteritems(), key=operator.itemgetter(0))
shit = []
for k,v in sorted_counts:
    time = int(k.strftime('%s'))
    if not s:
        g = time
        s = True
        time = 0
    else:
        time = time - g
    
    time = time / 100000.0
    shit.append([time, v])

print json.dumps(shit)
