from pymongo import Connection

c = Connection('localhost', 27018)
db = c['body_words']
body_words = db['all_body_words']
db = c['title_words']
title_words = db['all_title_words']

explored = set()

db = c['cached_entries']
cached_body_words = db['body_words']

count = 0
for word_obj in body_words.find():
    cached_body_words.ensure_index('word')
    if word_obj['word'] in explored or cached_body_words.find({'word' : word_obj['word']}).count():
        if word_obj['word'] not in explored:
            count += 1
            print 'count = ' + str(count)
        explored.add(word_obj['word'])
        continue
    else:
        print 'working on ' + word_obj['word']
        to_add = []
        all_matches = body_words.find({'word' : word_obj['word']})
        if all_matches.count() > 20000:
            print 'skipped ' + word_obj['word']
            explored.add(word_obj['word'])
            continue
        for article_to_add in all_matches:
            to_add.append({'word' : word_obj['word'], 'percentage' : article_to_add['percentage'], 'date' : article_to_add['date']})
        explored.add(word_obj['word'])
        cached_body_words.insert(to_add)
        
