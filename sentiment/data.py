"""Functions for reading data from the sentiment dictionary."""

import os

DATA_PATH = 'data' + os.sep

def load_sentiments(file_name="data"+os.sep+"sentiments.csv"):
    """Read the sentiment file and return a dictionary containing the sentiment
    score of each word, a value from -1 to +1.
    """
    sentiments = {}
    for line in open(file_name):
        word, score = line.split(',')
        sentiments[word] = float(score.strip())
    return sentiments

word_sentiments = load_sentiments()