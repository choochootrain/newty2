import random
import json
import datetime
import operator
import sys
from operator import itemgetter
if len(sys.argv) == 1:
    print 'need to specify prune percentage. suggest .2'
    sys.exit(1)
prune_percentage = float(sys.argv[1])
f = open('apple_articles.json', 'r')
articles = json.loads(f.read()) #[[date, word_counts], [date, word_counts]]
f.close()
f = open('AAPL.json', 'r')
dates_and_good_days_dict = json.loads(f.read())
f.close()
for article in articles:
    while article[0] not in dates_and_good_days_dict:
        date = datetime.datetime.strptime(article[0], '%m/%d/%Y')
        date += datetime.timedelta(days=1)
        article[0] =  date.strftime('%m/%d/%Y')
    article.append(dates_and_good_days_dict[article[0]])
    article.append(0)
#now articles [[date, word_counts, label, column_word_count],...]
print 'size of dates and good days dict', float(sys.getsizeof(dates_and_good_days_dict)) / 1000, 'kilobytes'
del dates_and_good_days_dict

words_to_article_count = {}
for date, word_counts, label, column_word_count in articles:
    for word in word_counts.keys():
        words_to_article_count[word] = words_to_article_count.get(word, 0) + 1

sorted_words_to_article_count = sorted(words_to_article_count.iteritems(), key=operator.itemgetter(1))
print len(sorted_words_to_article_count)
new_sorted_words_to_article_count = []
for i, word_and_count in enumerate(sorted_words_to_article_count):
    if word_and_count[1] >= 5:
        new_sorted_words_to_article_count.append(word_and_count)
print len(new_sorted_words_to_article_count)
#print new_sorted_words_to_article_count
del sorted_words_to_article_count
words_to_use = set()
for word, count in new_sorted_words_to_article_count:
    words_to_use.add(word)
words_to_use = list(words_to_use)
counter = 0
for article in articles:
    counter += 1
    print counter
    for word in article[1].keys():
        if word not in words_to_use:
            del article[1][word]




#now articles [[date,word_wcounts, good_day(label)]...]
#print articles


class decision_node:
    def __init__(self, col=-1, value=None, false_node=None, true_node=None, result=None):
        self.col = col
        self.value = value
        self.result = result
        self.true_node = true_node
        self.false_node = false_node


def majority_vote(results):
        if 1 in results and (0 not in results or results[1] > results[0]):
            return 1
        elif 0 in results and (1 not in results or results[0] > results[1]):
            return 0
        else: #Flip a coin
            return random.choice([0,1])



def entropy_counts(counts):
    from math import log
    log_2 = lambda x: log(x)/log(2)
    entropy = 0.0
    total = counts[0] + counts[1]
    if counts[0] > 0:
        p = float(counts[0]) / total
        entropy = entropy - p * log_2(p)
    if counts[1] > 0:
        p = float(counts[1]) / total
        entropy = entropy - p * log_2(p)
    return entropy

def entropy(articles):
    from math import log
    log_2 = lambda x: log(x)/log(2)
    counts = [0, 0]
    for article in articles:
        counts[article[2]] += 1
    zeros = counts[0]
    ones = counts[1]
    entropy = 0.0
    total = len(articles)
    if zeros > 0:
        p = float(zeros) / total
        entropy = entropy - p * log_2(p)
    if ones > 0:
        p = float(ones) / total
        entropy = entropy - p * log_2(p)
    return entropy

def build_tree(articles):
    print 'reached'
    if len(articles) == 0: return decision_node()
    current_score = entropy(articles)
    best_gain = 0
    best_criteria = None
    best_sets = None
    #labels = rows.T[len(rows[0]) - 1]
    num_articles = len(articles)
    for column_word in words_to_use:
        counts_left = [0, 0]
        counts_right = [0, 0]
        articles_with_column_word = []
        #now articles [[date, word_counts, label, column_word_count],...]
        for article in articles:
            if column_word not in article[1]:
                counts_left[article[2]] += 1
            else:
                counts_right[article[2]] += 1
                article[3] = article[1][column_word]
                articles_with_column_word.append(article)
        articles_with_column_word = sorted(articles_with_column_word, key=itemgetter(3))

        zeros  = float(counts_left[0] + counts_left[1])

        for i, article in enumerate(articles_with_column_word):
            if i == 0 or articles_with_column_word[i - 1][3] != article[3]:
                p = float(i + zeros) / num_articles
                gain = current_score - p * entropy_counts(counts_left) - (1 - p) * entropy_counts(counts_right)
                if gain > best_gain:
                    best_gain = gain
                    best_criteria = (column_word, article[3])
            counts_left[article[2]] += 1
            counts_right[article[2]] -= 1
    if best_gain > prune_percentage:
        best_sets = divide_set(articles, best_criteria[0], best_criteria[1])
        true_node = build_tree(best_sets[0])
        false_node = build_tree(best_sets[1])
        return decision_node(col=best_criteria[0], value=best_criteria[1], true_node = true_node, false_node = false_node)
    else:
        return decision_node(result = unique_results(articles))


def unique_results(articles):
    #can simplify this by checking if the last row all equals 0 or all equals 1
    results = {}
    if len(articles) == 0:
        return results
    for article in articles:
        results[article[2]] = results.get(article[2], 0) + 1
    return results


def divide_set(articles, word, value):
    true_set = []
    false_set = []
    for article in articles:
        if article[1].get(word, 0) >= value:
            true_set.append(article)
        else:
            false_set.append(article)
    return true_set, false_set

def print_tree(tree, indent=''):
    if tree.result != None:
        print str(tree.result)
    else:
        print str(tree.col) + ':'+ str(tree.value) +'? '
        print indent+'T->',
        print_tree(tree.true_node, indent + '    ')
        print indent+'F->',
        print_tree(tree.false_node, indent + '    ')


def test_tree(tree, articles):
    correct = 0
    for article in articles:
        word_counts = article[1]
        result = predict_tree(tree, word_counts)
        if result == article[2]:
            correct += 1
    print float(correct) / len(articles)

def predict_tree(tree, word_counts):
    current_node = tree
    while current_node.result == None:
        if word_counts.get(current_node.col, 0) >= current_node.value:
            current_node = current_node.true_node
        else:
            current_node = current_node.false_node
    return majority_vote(current_node.result)



def build_random_forest(articles, num_trees):
    forest = set()
    num_data_points = int(0.7 * len(articles))
    for i in range(num_trees): # For each tree
        # First permute rows
        random.shuffle(articles)
        # Select 70% of permuted rows as training data for tree
        random_training_data = articles[0:int(len(articles) * .70)]
        tree = build_random_tree(random_training_data)
        forest.add(tree)
        print 'New tree planted in forest'
    return forest


def predict_forest(forest, word_counts):
    result0 = 0
    result1 = 0
    for tree in forest:
        result = predict_tree(tree, word_counts)
        if result == 0:
            result0 += 1
        else:
            result1 += 1
    #Majority vote
    if result0 > result1:
        return 0
    elif result0 < result1:
        return 1
    else: #Flip a coin
        return random.choice([0,1])

def test_forest(forest, articles):
    correct = 0
    for article in articles:
        result = predict_forest(forest, articles[1])
        if result == article[2]:
            correct += 1
    print 'random forest results', float(correct) / len(data)


random.shuffle(articles)
training_set = articles[:len(articles) * 5 / 7]
testing_set = articles[len(articles) * 5 / 7 : ]

tree = build_tree(training_set)
print_tree(tree)
print 'on training set'
test_tree(tree, training_set)
print 'on testing set'
test_tree(tree, testing_set)
