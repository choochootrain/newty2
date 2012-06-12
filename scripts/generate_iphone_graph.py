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
path = "M0,500"

offset_time = int(sorted_counts[0][0].strftime('%s'))
counter = 0
total = 0
for k,v in sorted_counts:
    if counter == 5:
        graph_average_time = int(k.strftime('%s')) - offset_time
    if counter == 10:
        shit.append([graph_average_time / 70000.0, total])
        path += "L" + str(graph_average_time  / 70000.0) + ',' + str(total * 5)
        total = 0
        counter = 0
    total += v
    
    
    counter += 1        

print json.dumps(shit)
print "\n\n\n\n\n\n\n\n\n\n"
print path
