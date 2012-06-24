from pymongo import Connection
import json
useless_words_file = open('useless_words.json', 'r')
useless_words = set(json.load(useless_words_file))
useless_words_file.close()

word_counts_per_article_file = open('word_counts_per_article.json', 'r')
'''body_word_counts (dictionary of key words, value counts),
 header_word_counts (dictionary of key words, value counts),
 total_body_count (total number words in body),
 total_title_count (total number words in title),
 article_url'''

c = Connection('localhost', 27018)
db = c['all_articles']
coll = db['techcrunch.com']
coll.ensure_index('url')
word_count_per_article = []





body_words = c['body_words']
title_words = c['title_words']
#all_body_words = body_words['all_body_words']
#all_title_words = title_words['all_title_words']
def write_article_to_db(article_obj):
    for word, count in article_obj['body_word_counts'].items():
        if word in useless_words:
            continue
        coll = body_words[word]
        coll.insert({'article_id' : article_obj['_id'], 'total_num_words' : article_obj['total_body_count'], 'total_num_matched' : count, 'percentage' : float(count) / article_obj['total_body_count'], 'date' : article_obj['date']})
    for word, count in article_obj['header_word_counts'].items():
        if word in useless_words:
            continue
        coll = title_words[word]
        coll.insert({'article_id' : article_obj['_id'], 'total_num_words' : article_obj['total_title_count'], 'total_num_matched' : count, 'percentage' : float(count) / article_obj['total_title_count'], 'date' : article_obj['date']})



count = 0
for line in word_counts_per_article_file.readlines():
    count += 1
    if count % 10 == 0:
        print 'finished ' + str(count) + ' articles'
    article_obj = json.loads(line)
    article_ref = coll.find({'url' : article_obj['article_url']})[0]
    article_obj['_id'] = article_ref['_id']
    article_obj['date'] = article_ref['date']
    write_article_to_db(article_obj)
    del article_obj
word_counts_per_article_file.close()


