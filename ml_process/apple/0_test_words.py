from pymongo import Connection
import json
import re

c = Connection('localhost', 27018)
db = c['all_articles']
nytimes_articles = db['nytimes.com']
nytimes_errors = db['error_nytimes.com']
print 'Total number of articles ', nytimes_articles.count()

only_alphanumeric = re.compile('[\W_]+')


db = c['all_articles']
coll = db['techcrunch.com']


test_db = c['test']
nytimes_apple_articles = test_db['apple_articles']

def get_all_counts():
    article_count = 0
    c = Connection('localhost', 27018)
    title_word_counts = {}
    body_word_counts  = {}
    total_num_body_words = 0
    total_num_title_words = 0
    counter = 0
    for article in nytimes_articles.find():
        counter += 1
        if counter % 1000 == 0:
            print counter
        body = only_alphanumeric.sub(' ', article['body'].replace(u'\u00A0', ' ').lower())
        title = only_alphanumeric.sub(' ', article['title'].replace(u'\u00A0', ' ').lower())
        #words_in_body, total_body_count = get_counts(body, body_word_counts)
        #words_in_title, total_title_count = get_counts(title, title_word_counts)

        #if 'apple' in words_in_body and words_in_body['apple'] >= 4:
        words = body.split(' ')
        apple_count = words.count('apple')
        if apple_count >= 3:
            print article['title']
            article_count += 1
            print 'article count is ' , article_count
            nytimes_apple_articles.insert({'title': article['title'], 'body' : article['body'], 'url' : article['url'], 'apple_count' : apple_count, 'date' : article['date']})

        #total_num_body_words += total_body_count
        #total_num_title_words += total_title_count
    return body_word_counts, title_word_counts

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

    for word, count in words_in_text.items():
        significant_to_article = 1 if count > 3 else 0
        sig_to_article5 = 1 if count > 5 else 0
        sig_to_article10 = 1 if count > 10 else 0
        sig_to_article15 = 1 if count > 15 else 0
        sig_to_article25 = 1 if count > 25 else 0
        if word in word_counts:
            word_counts[word][0] += count
            word_counts[word][1] += significant_to_article
            word_counts[word][2] += sig_to_article5
            word_counts[word][3] += sig_to_article10
            word_counts[word][4] += sig_to_article15
            word_counts[word][5] += sig_to_article25
        else:
            word_counts[word] = [count, significant_to_article, sig_to_article5, sig_to_article10, sig_to_article15, sig_to_article25]
    return words_in_text, len(words)


if __name__ == '__main__':
    body_word_counts, title_word_counts = get_all_counts()
    body_word_counts = [[k, body_word_counts[k]] for k in sorted(body_word_counts)]
    title_word_counts = [[k, title_word_counts[k]] for k in sorted(title_word_counts)]
    '''
    f = open('body_word_counts.json', 'w')
    for x in body_word_counts:
        f.write(json.dumps(x) + '\n')
    f.close()
    f = open('title_word_counts.json', 'w')
    for x in title_word_counts:
        f.write(json.dumps(x) + '\n')
    f.close()
'''
