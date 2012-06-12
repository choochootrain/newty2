from pymongo import Connection, DESCENDING, ASCENDING
import sys
import operator
print 'columns are total_words, percentages, date, newspaper, word_count'

c = Connection('localhost', 27018)
db = c['words']
iphone = db[sys.argv[1]]


threshold = float(sys.argv[2])
counts_per_date = {}
for entry in iphone.find():
    date = entry['date']
    percentage = entry['percentage']
    if percentage > threshold:
        if date in counts_per_date:
            counts_per_date[date] += 1
        else:
            counts_per_date[date] = 1

sorted_counts = sorted(counts_per_date.iteritems(), key=operator.itemgetter(1))

for k,v in sorted_counts:
    print k, v
