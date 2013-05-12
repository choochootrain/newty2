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
f = open('apple_articles_clean.json', 'r')
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

del dates_and_good_days_dict
words_to_use = set()
for article in articles:
    for word in article[1].keys():
        words_to_use.add(word)


words_to_use = list(words_to_use)






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
        if 1 in results and (0 not in results or num_negative_articles * results[1] > num_positive_articles * results[0]):
            return 1
        elif 0 in results and (1 not in results or num_positive_articles * results[0] > num_negative_articles * results[1]):
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


def build_random_tree(articles):
    if len(articles) == 0: return decision_node()
    current_score = entropy(articles)
    best_gain = 0
    best_criteria = None
    best_sets = None
    #random.shuffle(words_to_use)
    num_articles = len(articles)
    #for column_word in words_to_use[:int(len(words_to_use) * .80)]:
    for column_word in words_to_use:
        counts_left = [0, 0]
        counts_right = [0, 0]
        articles_with_column_word = []
        random.shuffle(articles)
        random_article_set = articles[:int(len(articles) * .70)]
        #now articles [[date, word_counts, label, column_word_count],...]
        for article in random_article_set:
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
        result = predict_forest(forest, article[1])
        if result == article[2]:
            correct += 1
    print 'random forest results', float(correct) / len(articles)


random.shuffle(articles)
positive_articles = []
negative_articles = []
for article in articles:
    if article[2] == 0:
        negative_articles.append(article)
    else:
        positive_articles.append(article)
num_positive_articles = len(positive_articles)
num_negative_articles = len(negative_articles)
training_set = positive_articles[:num_positive_articles*2/3] + negative_articles[:num_negative_articles*2/3]
testing_set = positive_articles[num_positive_articles * 2 / 3:] + negative_articles[num_negative_articles * 2 /3:]
#training_set = articles[:len(articles) * 5 / 7]
#testing_set = articles[len(articles) * 5 / 7 : ]

print 'start'
tree = build_tree(training_set)
print_tree(tree)
print 'on training set'
test_tree(tree, training_set)
testing_set_positive = []
testing_set_negative = []
for article in testing_set:
    if article[2] == 0:
        testing_set_negative.append(article)
    else:
        testing_set_positive.append(article)
print len(testing_set_positive), 'positive length'
print len(testing_set_negative), 'negative length'
print 'on testing set positive'
test_tree(tree, testing_set_positive)
print 'on testing set negative'
test_tree(tree, testing_set_negative)
print 'finish'

forest = build_random_forest(training_set, 10)
print 'testing forest'
test_forest(forest, testing_set)
print 'testing forest on positive'
test_forest(forest, testing_set_positive)
print 'testing forest on negative'
test_forest(forest, testing_set_negative)




def build_weak_tree(articles):
    return build_tree(articles)

def error(weak_learner, D, articles):
    error = 0
    m = len(rows)
    for i in range(m):
        if predict_tree(weak_learner, rows[i]) != rows[i][57]:
            error += D[i]
            #error += 1.0/m
    return error



def adaboost(training_data_and_labels, T):
    m = len(training_data_and_labels)
    D = numpy.zeros(m)
    # Initialize D_1(i) = 1/m
    D += 1.0/m
    depth = 3 # Depth of weak learner tree
    weak_learners = []
    alphas = []
    indices = [i for i in range(m)]
    for t in range(0, T):
        sample_training_indices = numpy.random.choice(indices, 1000, replace=True, p=D)
        sample_training_data_and_labels = []
        #print sample_training_indices
        for i in sample_training_indices:
            sample_training_data_and_labels.append(training_data_and_labels[i])
        #print numpy.array(sample_training_data_and_labels).T[57]
        sample_training_data_and_labels = numpy.array(sample_training_data_and_labels)
        weak_learner = build_weak_tree(sample_training_data_and_labels, depth)
        #print_tree(weak_learner)
        e = error(weak_learner, D, training_data_and_labels)
        alpha = 0.5 * math.log((1.0 - e) / e)
        # Update weights
        results = []
        for row in training_data_and_labels:
            results.append((predict_tree(weak_learner, row) - 1.0/2) * 2)
        #print (training_data_and_labels.T[-1].T - 1.0 / 2) * 2
        D = D * numpy.exp(-alpha * ((training_data_and_labels.T[-1].T -1.0/2) * 2) * results)
        D = D / sum(D)
        #print list(D)
        weak_learners.append(weak_learner)
        alphas.append(alpha)
    return weak_learners, alphas


def test_adaboost(test_data_and_labels, weak_learners, alphas):
    correct = 0
    count = 0
    neg_count = 0
    #print alphas
    for data_and_label in test_data_and_labels:
        result = 0
        for i, weak_learner in enumerate(weak_learners):
            result += alphas[i] * (predict_tree(weak_learner, data_and_label) - 1.0/2) * 2
            x =  (predict_tree(weak_learner, data_and_label) - 1.0/2) * 2
            if x > 0:
                count += 1
            else:
                neg_count += 1

        if result > 0 and data_and_label[-1] == 1:
            correct += 1
        if result < 0 and data_and_label[-1] == 0:
            correct += 1
    #print count, neg_count
    print float(correct) / len(test_data_and_labels), 'correct for adaboost'

if 'finished adaboost' == True:
    print 'start adaboost'
    weak_learners, alphas = adaboost(training_data, 40)
    print 'test on training data'
    test_adaboost(training_data, weak_learners, alphas)
    print 'test on testing data'
    test_adaboost(test_data, weak_learners, alphas)
    print 'test on testing set positive'
    test_adaboost(testing_set_positive, weak_learners, alphas)
    print 'test on testing set negative'
    test_adaboost(testing_set_negative, weak_learners, alphas)
