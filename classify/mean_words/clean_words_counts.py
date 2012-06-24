from pymongo import Connection
import json
import re
c = Connection('localhost', 27018)
db = c['all_articles']
coll = db['techcrunch.com']
f = open('body_word_counts', 'r')
body_word_counts = json.load(f)
f.close()

clean_body_word_counts = {}
useless_words = []
for word, value in body_word_counts.items():
    if value[0] > 10:
        clean_body_word_counts[word] = value
    else:
        useless_words.append(word)
f = open('clean_body_word_counts.json', 'w')
f.write(json.dumps(clean_body_word_counts))
f.close()


f = open('useless_words.json', 'w')
f.write(json.dumps(useless_words))
f.close()
