from pymongo import Connection
import json
import re
import numpy
only_alphanumeric = re.compile('[\W_]+')

f = open('removed_words.json', 'r')
removed_words = set(json.loads(f.read()))


c = Connection('localhost', 27018)
test_db = c['test']
nytimes_apple_articles = test_db['apple_articles']
nytimes_apple_articles.ensure_index('date')

body_words = set()
title_words = set()
for article in nytimes_apple_articles.find():
    body = only_alphanumeric.sub(' ', article['body'].replace(u'\u00A0', ' ').lower())
    words = body.split(' ')
    for word in words:
        if word not in removed_words:
            body_words.add(word)
    title = only_alphanumeric.sub(' ', article['title'].replace(u'\u00A0', ' ').lower())
    words = title.split(' ')
    for word in words:
        if word not in removed_words:
            title_words.add(word)

body_words = list(body_words)
title_words = list(title_words)
print 'number of body words is', len(body_words)
print 'number of title words is', len(title_words)




def get_counts(text, word_counts):
    words_in_text = {}
    words = text.split(' ')
    for word in words:
        word = only_alphanumeric.sub(' ', word.lower())
        word = word.strip()
        if len(word) <= 1:
            continue
        if word in words_in_text:
            words_in_text[word] += 1
        else:
            words_in_text[word] = 1
    return words_in_text, len(words)




date_to_counts = {}
for i, article in enumerate(nytimes_apple_articles.find().sort('date')):
    print 'reached article', i
    body = only_alphanumeric.sub(' ', article['body'].replace(u'\u00A0', ' ').lower())
    title = only_alphanumeric.sub(' ', article['title'].replace(u'\u00A0', ' ').lower())
    words_in_body, total_body_count = get_counts(body, {})
    words_in_title, total_title_count = get_counts(title, {})
    if article['date'] not in date_to_counts:
        date_to_counts[article['date']] = numpy.zeros(len(body_words) + len(title_words))
    for word, count in words_in_body.items():
        if word in removed_words:
            continue
        date_to_counts[article['date']][body_words.index(word)] += count
    for word, count in words_in_title.items():
        if word in removed_words:
            continue
        date_to_counts[article['date']][len(body_words) + title_words.index(word)] += count


output_array = [numpy.concatenate([body_words, title_words, [0]])]

date_keys = date_to_counts.keys()
date_keys.sort()
print len(date_keys)
for date in date_keys:
    date_counts_row = [numpy.concatenate([date_to_counts[date], [date]])]
    print numpy.shape(output_array), numpy.shape(date_counts_row)
    output_array = numpy.append(output_array, date_counts_row, axis=0)
    del date_to_counts[date]

print output_array

f = open('apple_articles.npy', 'w')
numpy.save(f, output_array)
f.close()
