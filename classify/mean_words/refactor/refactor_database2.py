from pymongo import Connection

c = Connection('localhost', 27018)
db = c['body_words']
body_words = db['all_body_words']
db = c['title_words']
title_words = db['all_title_words']



db = c['fast_entries']
cached_body_words = db['body_words']

ah = set(['a','b','c','d','e','f','g','h'])
ir = set(['i','j','k','l','m','n','o','p','q','r'])
sz = set(['s','t','u','v','w','x','y','z'])

count = 0
def run(letters):
    global count
    explored = {}
    for word_obj in body_words.find():
        word = word_obj['word']
        if word[:1] not in letters:
            continue
        count += 1
        if count % 1000:
            print 'finished ' + str(count)
        if word in explored:
            #explored[word].append((word_obj['percentage'], word_obj['date'], word_obj['total_num_matched']))
            explored[word].append((word_obj['percentage'], word_obj['date']))
        else:
            #explored[word] = [(word_obj['percentage'], word_obj['date'], word_obj['total_num_matched']),]
            explored[word] = [(word_obj['percentage'], word_obj['date']),]

    for word, word_obj in explored.items():
        if len(word_obj) > 20000:
            continue
        cached_body_words.insert({'word' : word, 'info' : word_obj})

run(ah)
run(ir)
run(sz)
