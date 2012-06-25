from application1.models import NewsSource, Article, BodyIndex, TitleIndex, ErrorsParsing
import json
import re
only_alphanumeric = re.compile('[\W_]+')
all_title_words = {}
all_body_words = {}
def get_all_counts():
    counter = 0
    for article in Article.objects.all():
        counter += 1
        print '\r' + str(counter)
        words_in_body, total_body_count = get_counts(only_alphanumeric.sub(' ', article.body.replace(u'\u00A0', ' ').lower()), all_body_words)
        words_in_title, total_title_count = get_counts(only_alphanumeric.sub(' ', article.title.replace(u'\u00A0', ' ').lower()), all_title_words)
        f = open('word_counts_per_article', 'a')
        f.write(json.dumps({'article_url' : article.url, 'body_word_counts' : words_in_body,
                            'header_word_counts' : words_in_title, 'total_body_count' : total_body_count, 'total_title_count' : total_title_count}) + '\n')
        f.close()
        
    return all_title_words, all_body_words

def get_counts(text, all_words):
    words_in_text = {}
    words = text.split(' ')
    for word in words:
        word = only_alphanumeric.sub(' ', word.lower())
        if word == '':
            continue
        if word in words_in_text:
            words_in_text[word] += 1
        else:
            words_in_text[word] = 1

    total_count = len(words)
    #print total_count, len(words_in_text)
    for word, count in words_in_text.items():
        if word in all_words:
            all_words[word][0] += count
            all_words[word][1] += total_count
        else:
            all_words[word] = [count, total_count]
    return words_in_text, total_count


def main():
    counts = get_all_counts()
    f = open('body_word_counts', 'w')
    f.write(json.dumps(counts[1]))
    f.close()
    f = open('title_word_counts', 'w')
    f.write(json.dumps(counts[0]))
    f.close()
    

if __name__ == '__main__':
    counts = get_all_counts()
    f = open('body_word_counts', 'w')
    f.write(json.dumps(counts[1]))
    f.close()
    f = open('title_word_counts', 'w')
    f.write(json.dumps(counts[0]))
    f.close()
    """
    for k, v in get_word_counts().items():
        f.write(json.dumps([k, v]) + '\n')
    f.close()
    #for k, v in get_word_counts().items():
        #print {k, v
"""
