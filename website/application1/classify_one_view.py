import re
import codecs
import math
import sys
import os.path
from pymongo import Connection    


def main(newspaper_name, word_to_match):
    c = Connection('localhost', 27018)
    words_db = c['words']
    word_match_regex = re.compile(r'\b' + word_to_match + r'\b')

    newspaper_db_name = newspaper_name.replace('http://', '').replace('www.', '')
    article_db = c['all_articles']
    newspaper_coll = article_db[newspaper_db_name]

    if not handled(word_to_match, words_db):
        populate_word_list(newspaper_coll, newspaper_name, newspaper_db_name, word_to_match, words_db, word_match_regex)
        return True
    return True






to_remove = re.compile('\W+')
whitespace = re.compile('\s+')
def remove_useless_chars(text):
    text = to_remove.sub(' ', text)
    text = text.replace('_', ' ').replace('\n', ' ')
    text = whitespace.sub(' ', text)
    return text


def handled(word, words_db):
    word_coll = words_db[word]
    if word_coll.count() > 1:
        return True
    else:
        return False


def store_in_database(store_obj, words_db):
    print 'storing into database'
    for word, articles in store_obj.items():
        if word.isspace() or word == '':
            continue
        word_coll = words_db[word]
        word_coll.insert(articles)





def populate_word_list(newspaper_coll, newspaper_name, newspaper_db_name, word_to_match, words_db, word_match_regex):
    store_counter = 0
    temp_store_obj = {}
    for article_obj in newspaper_coll.find(timeout=False):
        if store_counter > 5000:
            store_in_database(temp_store_obj, words_db)
            del temp_store_obj
            temp_store_obj = {}
            store_counter = 0
        store_counter += 1
        
        obj_id = article_obj['_id']
        body = article_obj['body']
        title = article_obj['title']
        #print 'working on ' + title
        url = article_obj['url']
        file_path = article_obj['file_path']
        date = article_obj['date']
        
        text_to_eval = body.strip().lower() + ' ' +  title.strip().lower()
        text_to_eval = remove_useless_chars(text_to_eval)
        
        #specific shit
        if not word_to_match in text_to_eval:
            continue

        total_num_matched = len(word_match_regex.findall(text_to_eval))
        total_num_words = len(whitespace.split(text_to_eval))
        word_analysis = {'total_num_words' : total_num_words, 'total_num_matched' : total_num_matched, 'percentage' : float(total_num_matched) / total_num_words, 'article_id' : obj_id, 'newspaper' : newspaper_db_name, 'date' : date}
        if word_to_match in temp_store_obj:
            temp_store_obj[word_to_match].append(word_analysis)
        else:
            temp_store_obj[word_to_match] = [word_analysis,]
        
    



if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
