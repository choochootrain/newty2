import json
import operator

f = open('apple_articles.json', 'r')
articles = json.loads(f.read())
f.close()

words_to_article_count = {}
for date, word_counts in articles:
    for word in word_counts.keys():
        words_to_article_count[word] = words_to_article_count.get(word, 0) + 1

words_to_article_count = sorted(words_to_article_count.iteritems(), key=operator.itemgetter(1))
words_to_use = []
for i, word_and_count in enumerate(words_to_article_count):
    if word_and_count[1] >= 5:
        words_to_use.append(word_and_count[0])
counter = 0
for article in articles:
    counter += 1
    print counter
    for word in article[1].keys():
        if word not in words_to_use:
            del article[1][word]
articles_to_write = json.dumps(articles)
f = open('apple_articles_clean.json', 'w')
f.write(articles_to_write)
f.close()
