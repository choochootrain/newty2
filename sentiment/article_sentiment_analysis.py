'''
Sentiment analysis adapted from basic_sentiment_analysis.py and trends.py
'''

from pprint import pprint
from data import word_sentiments # word_sentiments is a dictionary of words with a sentiment between -1 (negative) to 1 (positive)
import nltk
import os
import re
from collections import Counter
from pandas import DataFrame

f = open('techcrunch_articles.csv', 'rb')
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
    # Step 2: Update Sentiment
    sentiment = 0
    for word in bag:
        if word in word_sentiments.keys():
            sentiment += word_sentiments[word] * bag[word] # creates weighted sum of sentiment, based upon the nubmer of times that word appeared.
    return sentiment / sum(bag.values())

if __name__ == '__main__':
    articles = tc_data['body']
    d = dict()
    for article in articles:
        cleaned_article = clean_words(article)
