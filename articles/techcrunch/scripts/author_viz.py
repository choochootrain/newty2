import csv
import datetime
import json
from collections import Counter, defaultdict

file = 'techcrunch_articles.csv'

days = defaultdict(list)
data = {}

reader = csv.reader(open(file), delimiter=',')
reader.next()
for row in reader:
  link = row[0]
  title = row[1]
  author = row[2]

  parts = link.split('/')
  date = datetime.datetime(int(parts[3]), int(parts[4]), int(parts[5]))

  days[date].append(author)

keys = days.keys()
keys.sort()

for date in keys:
  data[date.isoformat()] = Counter(days[date])

print json.dumps(data, sort_keys=True)
