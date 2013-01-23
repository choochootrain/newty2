from pymongo import Connection, ASCENDING, DESCENDING
c = Connection('localhost', 27018)
db = c['all_articles']
body_words = c['body_words']
title_words = c['title_words']
body_words = body_words['all_body_words']
title_words = title_words['all_title_words']
body_words.ensure_index('article_id')
print 'finished'
body_words.ensure_index('percentage')
print 'finished'
body_words.ensure_index('date')
print 'finished'
body_words.ensure_index('total_num_matched')
print 'finished'
body_words.ensure_index([('date', DESCENDING), ('word', DESCENDING)])

title_words.ensure_index('article_id')
print 'finished'
title_words.ensure_index('percentage')
print 'finished'
title_words.ensure_index('date', DESCENDING)
print 'finished'
title_words.ensure_index('total_num_matched')
print 'finished'
title_words.ensure_index('word')
print 'finished'
body_words.ensure_index('word')
print 'finished'

db = c['fast_entries']
cached_body_words = db['body_words']
cached_body_words.ensure_index('word')
