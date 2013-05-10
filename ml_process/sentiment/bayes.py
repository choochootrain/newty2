# sample bayes classifier training
# TODO: adapt this for use with article data

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from os import listdir
from os.path import isfile, join

def word_feats(words):
  return dict([(word, True) for word in words])

def wordize(f):
  lines = [line.strip() for line in open(f)]
  lines = map(lambda x: x.split(' '), lines)
  return [item for sublist in lines for item in sublist]

negfiles = [ join('neg', f) for f in listdir('neg') if isfile(join('neg',f)) ]
posfiles = [ join('pos', f) for f in listdir('pos') if isfile(join('pos',f)) ]

negfeats = [(word_feats(wordize(f)), 'neg') for f in negfiles]
posfeats = [(word_feats(wordize(f)), 'pos') for f in posfiles]

negcutoff = len(negfeats)*3/4
poscutoff = len(posfeats)*3/4

trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

classifier = NaiveBayesClassifier.train(trainfeats)
print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
classifier.show_most_informative_features()
