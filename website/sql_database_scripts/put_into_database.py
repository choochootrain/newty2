from application1.models import NewsSource, Article, BodyIndex, TitleIndex, ErrorsParsing
#from pymongo import Connection
import json
from django.db import transaction
useless_words_file = open('useless_words.json', 'r')
useless_words = set(json.load(useless_words_file))
useless_words_file.close()

word_counts_per_article_file = open('word_counts_per_article.json', 'r')
'''body_word_counts (dictionary of key words, value counts),
 header_word_counts (dictionary of key words, value counts),
 total_body_count (total number words in body),
 total_title_count (total number words in title),
 article_url'''


word_count_per_article = []





#body_words = c['body_words']
#title_words = c['title_words']
def write_article_to_db(article_obj):
    for word, count in article_obj['body_word_counts'].items():
        if word in useless_words:
            continue
        #new_body_index = BodyIndex(article = article_obj['ref'], word_count = count, total_word_count = article_obj['total_body_count'],
        #percentage = float(count) / article_obj['total_body_count'], date = article_obj['date'], word = word)
        new_body_index = BodyIndex(article = article_obj['ref'], word_count = count, total_word_count = article_obj['total_body_count'],
                                   percentage = float(count) / article_obj['total_body_count'], word = word)


        new_body_index.save()
    for word, count in article_obj['header_word_counts'].items():
        if word in useless_words:
            continue
        #new_title_index = TitleIndex(article = article_obj['ref'], word_count = count, total_word_count = article_obj['total_title_count'],
        #                             percentage = float(count) / article_obj['total_title_count'], date = article_obj['date'], word = word)

        new_title_index = TitleIndex(article = article_obj['ref'], word_count = count, total_word_count = article_obj['total_title_count'],
                                     percentage = float(count) / article_obj['total_title_count'], word = word)
        
        new_title_index.save()

@transaction.commit_manually
def main():
    count = 0
    for line in word_counts_per_article_file.readlines():
        count += 1
        if count <= 44000:
            continue
        if count > 60000:
            continue
        if count % 100 == 0:
            transaction.commit()
        if count % 10 == 0:
            print 'finished ' + str(count) + ' articles'
        article_obj = json.loads(line)
        article_ref = Article.objects.filter(url = article_obj['article_url'])[0]
    #article_ref = coll.find({'url' : article_obj['article_url']})[0]
        article_obj['ref'] = article_ref
        article_obj['date'] = article_ref.date
        write_article_to_db(article_obj)
        del article_obj
    word_counts_per_article_file.close()



main()
