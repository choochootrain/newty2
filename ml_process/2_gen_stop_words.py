import json
f = open('stop_words.txt', 'r')
stop_words = []
for line in f:
    stop_words.append(line.lower().split("'")[0].strip())
f.close()
f = open('stop_words.json', 'w')
f.write(json.dumps(sorted(stop_words)))
f.close()
