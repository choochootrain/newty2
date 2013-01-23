import os
f = file('new_queue', 'r')
unique_queue = set()
count = 0
for line in f:
    count += 1
    if count % 1000 == 0:
        print count
    unique_queue.add(line.strip())
f.close()
os.remove('/scraped_news/nytimes.com/new_queue')
f = file('new_queue', 'w')
to_write = ''
for x in unique_queue:
    to_write += x + '/n'
f.write(to_write)
f.close()
