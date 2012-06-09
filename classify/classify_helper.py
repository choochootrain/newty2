import re
import codecs
import math
import sys
from pymongo import Connection
def percent_match(html, keywords):
    html_array = html.split(' ')
    total_length = len(html_array)
    num_matches = 0
    for keyword in keywords:
        num_matches += num_match(html, keyword)
    return num_matches / float(total_length)


def num_match(html, keyword):
    return len(re.findall(keyword, html))



"""gets mean occurence and standard deviation of an occurence of each keyword in keywords"""
"""returns {keyword1 : [mean, std_dev], keyword2 : [mean, std_dev]}"""
"""file_paths are the list of file_paths we are training on"""
def get_stats(file_paths, keywords):
    keywords_upper = []
    for x in keywords:
        keywords_upper.append(x.upper())
    keywords = keywords_upper

    result = {}
    """freq_table -> {keyword : [freq_file_1, freq_file2]}"""
    freq_table = {}
    for x in keywords:
        freq_table[x] = []
    for file in file_paths:
        f = codecs.open(file, 'r', 'iso-8859-1')
        html = ' ' + f.read().upper() + ' '
        for keyword in keywords:
            keyword_freq = html.count(' ' + keyword + ' ')
            freq_table[keyword].append(keyword_freq)

    for k, v in freq_table.items():
        mean = sum(v)/len(v)
        std_dev = math.sqrt(sum([(x - mean) ** 2 for x in v])/len(v))
        result[k] = (mean, std_dev)
    return result
    
        
to_remove = re.compile('\W+')
whitespace = re.compile('\s+')
def remove_useless_chars(text):
    text = to_remove.sub(' ', text)
    text = text.replace('_', ' ').replace('\n', ' ')
    text = whitespace.sub(' ', text)
    return text


c = Connection('localhost', 27018)
words_db = c['words']

def store_in_database(store_obj):
    print 'storing into database'
    for word, articles in store_obj.items():
        if word.isspace() or word == '':
            continue
        word_coll = words_db[word]
        for article in articles:
            word_coll.insert(article)

def populate_word_list(newspaper_name):
    newspaper_db_name = newspaper_name.replace('http://', '').replace('www.', '')
    article_db = c['all_articles']
    newspaper_coll = article_db[newspaper_db_name]
    store_counter = 0
    temp_store_obj = {}
    for article_obj in newspaper_coll.find():
        if store_counter > 1000:
            store_in_database(temp_store_obj)
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
        result_eval = eval_text(text_to_eval)
        total_words = result_eval['total_words']
        word_counts = result_eval['word_counts']
        for word in word_counts.keys():
            word_analysis = {'total_words' : total_words, 'word_count' : word_counts[word], 'percentage' : float(word_counts[word]) / total_words, 'article_id' : obj_id, 'title' : title, 'url' : url, 'file_path' : file_path, 'date' : date}
            #print word, word_analysis
            if word in temp_store_obj:
                temp_store_obj[word].append(word_analysis)
            else:
                temp_store_obj[word] = [word_analysis,]
        

def eval_text(text_to_eval):
    word_counts = {}
    word_array = text_to_eval.split(' ')
    total_words = len(word_array)
    for word in word_array:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
        
    return {'total_words' : total_words, 'word_counts' : word_counts}
    


if __name__ == '__main__':
    populate_word_list(sys.argv[1])
