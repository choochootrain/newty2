'''
Sentiment analysis adapted from basic_sentiment_analysis.py and trends.py
'''

from data import word_sentiments  # word_sentiments is a dictionary of words with a sentiment between -1 (negative) to 1 (positive)
import re
from collections import Counter
from pandas import DataFrame

f = open('articles/techcrunch_articles.csv', 'rb')
tc_data = DataFrame.from_csv(f, header=0)

regex = re.compile('            Learn more  End of panel-container -->')


def clean_words(text):
    '''Cleans corpus up, removing HTML and punctuation.'''
    cleaned_text = regex.sub('', text)
    return cleaned_text


def bag_of_words(words):
    return Counter(words.split())


def extract_article_sentiment(cleaned_text):
    # Step 1: Create Bag of Words
    bag = bag_of_words(cleaned_text)
    if sum(bag.values()) == 0:  # checking against the edge case of if there are no words in the article.
        return 0
    # Step 2: Update Sentiment
    sentiment = 0
    for word in bag:
        if word in word_sentiments.keys():
            sentiment += word_sentiments[word] * bag[word]  # creates weighted sum of sentiment, based upon the nubmer of times that word appeared.
    return sentiment / sum(bag.values())  # creates sentiment averaged over all unique words.


def normalize(sentiment):
    '''
    Normalizes sentiment value between -1 and 1 using min/max
    Both the minimum and maximum sentiment were calculated beforehand.
    '''
    max_sent = 0.116
    min_sent = -0.0625
    normalized_value = sentiment / (abs(max_sent) + abs(min_sent) / 2)
    return normalized_value


if __name__ == '__main__':
    articles = tc_data['body']
    data = []
    for article, index, author in zip(articles, tc_data.index, tc_data['author']):
        if article == article:
            article_dict = {}

            # Getting the sentiment value
            cleaned_article = clean_words(article)
            sentiment = extract_article_sentiment(cleaned_article)
            normalized_sentiment = normalize(sentiment)
            article_dict['link'] = index
            article_dict['sentiment'] = normalized_sentiment
            article_dict['author'] = author
            ## Getting the dates
            link = index.split('/')
            article_dict['date'] = (link[3] + '-' + link[4] + '-' + link[5])

            data.append(article_dict)
            print article_dict
