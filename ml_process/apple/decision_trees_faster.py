import scipy.io as sio
import numpy
import random
import sys
import math

#Authors: Lu Cheng, Victor Zhu, Ben Sklaroff

if len(sys.argv) > 1:

    part1 = '1' in sys.argv[1] # Decision Trees
    part2 = '2' in sys.argv[1] # Decision Trees with Pruning
    part3 = '3' in sys.argv[1] # Random Forests and Random Forests with Pruning
    part4 = '4' in sys.argv[1] # Adaboost
    part5 = '5' in sys.argv[1] # Extra Credit: Bagging
    part6 = '6' in sys.argv[1] # Extra Credit: Gini impurity
    part7 = '7' in sys.argv[1] # Extra Credit: Quadrary Decision Trees
    part8 = '8' in sys.argv[1] # Extra Credit: Cross Validation
else:
    part1 = True
    part2 = True
    part3 = True
    part4 = True
    part5 = True
    part6 = True
    part7 = True
    part8 = True

spam_data = sio.loadmat('spamData.mat')
training_data = numpy.float64(spam_data['Xtrain'])
training_labels = numpy.int_(list(spam_data['ytrain']))
test_data = numpy.float64(spam_data['Xtest'])
test_labels = numpy.int_(list(spam_data['ytest']))

training_data_and_labels = numpy.concatenate((training_data.T, training_labels.T)).T
test_data_and_labels = numpy.concatenate((test_data.T, test_labels.T)).T


class decision_node:
    def __init__(self, col=-1, value=None, false_node=None, true_node=None, result=None):
        self.col = col
        self.value = value
        self.result = result
        self.true_node = true_node
        self.false_node = false_node

def greaterThanVal(element, value):
    return element >= value

def lessThanVal(element, value):
    return element < value

def divide_set(rows, column_index, value):
    #this takes 2:38
    set1 = rows[greaterThanVal(rows[:, column_index], value)]
    set2 = rows[lessThanVal(rows[:, column_index], value)]
    #this takes 2:41
    #set1 = rows[rows[:, column_index] >= value]
    #set2 = rows[rows[:, column_index] < value]
    #set1 = numpy.split(rows, numpy.where(rows[:, column_index] >= value)[0])
    #set2 = numpy.split(rows, numpy.where(rows[:, column_index] < value)[0])
    #set1 = [row for row in rows if row[column_index] >= value]
    #set2 = [row for row in rows if row[column_index] < value]
    return (set1, set2)

def unique_results(rows):
    #can simplify this by checking if the last row all equals 0 or all equals 1
    results = {}
    if len(rows) == 0:
        return results
    ones = numpy.count_nonzero(rows.T[len(rows[0]) - 1])
    zeros = len(rows) - ones
    if zeros != 0:
        results[0] = zeros
    if ones != 0:
        results[1] = ones
    #for row in rows:
    #    if row[len(row) - 1] not in results:
    #        results[row[len(row) - 1]] = 1
    #    else:
    #        results[row[len(row) - 1]] += 1
    return results



def majority_vote(results):
    if len(results) == 1:
        if (0 in results):
            return 0
        else:
            return 1
    else:
        if results[0] > results[1]:
            return 0
        elif results[0] < results[1]:
            return 1
        else: #Flip a coin
            return random.choice([0,1])


def entropy(rows):
    from math import log
    log_2 = lambda x:log(x)/log(2)
    results = unique_results(rows)
    entropy = 0.0
    for r in results.keys():
        p = float(results[r]) / len(rows)
        entropy = entropy - p * log_2(p)
    return entropy



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


def build_tree(rows):
    if len(rows) == 0: return decision_node()
    current_score = entropy(rows)
    best_gain = 0.0
    best_criteria = None
    best_sets = None
    column_count = len(rows[0]) - 1
    labels = rows.T[len(rows[0]) - 1]
    for column_index in range(column_count):
        column_and_label = numpy.array([rows.T[column_index], labels.T]).T
        column_and_label = column_and_label[column_and_label[:,0].argsort()]
        counts_left = []
        counts_left.append(0)
        counts_left.append(0)
        counts_right = []
        counts_right.append(len(column_and_label) - numpy.count_nonzero(column_and_label.T[1]))
        counts_right.append(len(column_and_label) - counts_right[0])
        for i in range(len(column_and_label)):
            if i != 0 and column_and_label[i - 1][0] != column_and_label[i][0]:
                p = float(i)/len(column_and_label)
                gain = current_score - p * entropy_counts(counts_left) - (1 - p) * entropy_counts(counts_right)
                if gain > best_gain:# and i + 1 != len(column_and_label):
                    best_gain = gain
                    best_criteria = (column_index, column_and_label[i][0])
            if column_and_label[i][1] == 1:
                counts_left[1] += 1
                counts_right[1] -= 1
            else:
                counts_left[0] += 1
                counts_right[0] -= 1

    if best_gain > 0:
        best_sets = divide_set(rows, best_criteria[0], best_criteria[1])
        true_node = build_tree(best_sets[0])
        false_node = build_tree(best_sets[1])
        return decision_node(col=best_criteria[0], value=best_criteria[1], true_node = true_node, false_node = false_node)
    else:
        return decision_node(result = unique_results(rows))



def print_tree(tree, indent=''):
    if tree.result != None:
        print str(tree.result)
    else:
        print str(tree.col) + ':'+ str(tree.value) +'? '
        print indent+'T->',
        print_tree(tree.true_node, indent + '    ')
        print indent+'F->',
        print_tree(tree.false_node, indent + '    ')


def test_tree(tree, data, labels):
    correct = 0
    for i in range(0, len(data)):
        d = data[i]
        result = predict_tree(tree, d)
        if result == labels[i][0]:
            correct += 1
    print float(correct) / len(data)

def predict_tree(tree, data):
    current_node = tree
    while current_node.result == None:
        if data[current_node.col] >= current_node.value:
            current_node = current_node.true_node
        else:
            current_node = current_node.false_node
    return majority_vote(current_node.result)


if part1:
    print 'part 1: Decision trees'

    tree = build_tree(training_data_and_labels)


    print 'Full tree'
    test_tree(tree, test_data, test_labels)



def prune_tree(tree, mingain):
    # If branches aren't leaves, then prune them
    if tree.true_node.result==None:
        prune_tree(tree.true_node,mingain)
    if tree.false_node.result==None:
        prune_tree(tree.false_node,mingain)

    # If both the subbranches are now leaves, see if they
    # should be merged
    if tree.true_node.result!=None and tree.false_node.result!=None:
        # Build a combined dataset
        tb,fb=[],[]
        for v,c in tree.true_node.result.items():
            tb+=[[v]]*c
        for v,c in tree.false_node.result.items():
            fb+=[[v]]*c

        # Test the reduction in entropy
        delta=entropy(numpy.array(tb+fb))-(float(entropy(numpy.array(tb))+entropy(numpy.array(fb)))/2)
        if delta<mingain:
            #Merge the branches
            tree.true_node,tree.false_node=None,None
            tree.result=unique_results(numpy.array(tb+fb))



if part2:
    tree = build_tree(training_data_and_labels)
    print 'part 2: Decision Trees with pruning'
    prune_tree(tree,0.1)
    print 'Pruned tree with mingain = 0.1'
    test_tree(tree, test_data, test_labels)


    prune_tree(tree,0.2)
    print 'Pruned tree with mingain = 0.2'
    test_tree(tree, test_data, test_labels)

    prune_tree(tree,0.3)
    print 'Pruned tree with mingain = 0.3'
    test_tree(tree, test_data, test_labels)

    prune_tree(tree,0.4)
    print 'Pruned tree with mingain = 0.4'
    test_tree(tree, test_data, test_labels)

    prune_tree(tree,0.5)
    print 'Pruned tree with mingain = 0.5'
    test_tree(tree, test_data, test_labels)

    prune_tree(tree,0.6)
    print 'Pruned tree with mingain = 0.6'
    test_tree(tree, test_data, test_labels)

    prune_tree(tree,0.7)
    print 'Pruned tree with mingain = 0.7'
    test_tree(tree, test_data, test_labels)

    prune_tree(tree,0.8)
    print 'Pruned tree with mingain = 0.8'
    test_tree(tree, test_data, test_labels)

    prune_tree(tree,0.9)
    print 'Pruned tree with mingain = 0.9'
    test_tree(tree, test_data, test_labels)

    prune_tree(tree,1.0)
    print 'Pruned tree with mingain = 1.0'
    test_tree(tree, test_data, test_labels)


def predict_forest(forest, data):
    result0 = 0
    result1 = 0
    for tree in forest:
        result = predict_tree(tree, data)
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

def test_forest(forest, data, labels):
    correct = 0
    for i in range(0, len(data)):
        d = data[i]
        result = predict_forest(forest, d)
        if result == labels[i][0]:
            correct += 1
    print float(correct) / len(data)


def build_random_forest(rows, num_trees):
    forest = set()
    num_data_points = int(0.7 * len(rows))
    for i in range(0, num_trees): # For each tree
        # First permute rows
        permuted_rows = numpy.random.permutation(rows)
        # Select 70% of permuted rows as training data for tree
        random_training_data = permuted_rows[0:num_data_points]
        tree = build_random_tree(random_training_data)
        forest.add(tree)
        print 'New tree planted in forest'
    return forest



def build_random_tree(rows):
    if len(rows) == 0: return decision_node()
    current_score = entropy(rows)
    num_set = int(0.7*len(rows))
    best_gain = 0.0
    best_criteria = None
    best_sets = None
    column_count = len(rows[0]) - 1
    labels = rows.T[len(rows[0]) - 1]
    for column_index in range(column_count): #For every feature
        column_values = set()
        column_and_label = numpy.array([rows.T[column_index], labels.T]).T
        column_and_label = column_and_label[column_and_label[:,0].argsort()]
        random_rows = numpy.random.permutation(rows) # Permute again #modified
        random_rows = random_rows[0:num_set] # Select 70% of points to decide split #modified
        counts_left = []
        counts_left.append(0)
        counts_left.append(0)
        counts_right = []
        counts_right.append(len(column_and_label) - numpy.count_nonzero(column_and_label.T[1]))
        counts_right.append(len(column_and_label) - counts_right[0])

        for row in random_rows:#modified
            column_values.add(row[column_index])
        for i in range(len(column_and_label)):
            if i != 0 and column_and_label[i - 1][0] != column_and_label[i][0] and column_and_label[i][0] in column_values:
                p = float(i)/len(column_and_label)
                gain = current_score - p * entropy_counts(counts_left) - (1 - p) * entropy_counts(counts_right)
                if gain > best_gain:# and i + 1 != len(column_and_label):
                    best_gain = gain
                    best_criteria = (column_index, column_and_label[i][0])
            if column_and_label[i][1] == 1:
                counts_left[1] += 1
                counts_right[1] -= 1
            else:
                counts_left[0] += 1
                counts_right[0] -= 1

    if best_gain > 0:
        best_sets = divide_set(rows, best_criteria[0], best_criteria[1])
        true_node = build_random_tree(best_sets[0])
        false_node = build_random_tree(best_sets[1])
        return decision_node(col=best_criteria[0], value=best_criteria[1], true_node = true_node, false_node = false_node)
    else:
        return decision_node(result = unique_results(rows))

def prune_forest(forest, mingain):
    for tree in forest:
        prune_tree(tree, mingain)

if part3:
    print 'part 3: random forests'
    forest = build_random_forest(training_data_and_labels, 100)
    test_forest(forest, test_data, test_labels)
    print 'Random forests with pruning'
    prune_forest(forest, 0.6)
    test_forest(forest, test_data, test_labels)

#Adaboost

# Create a small tree
def build_weak_tree(rows, depth):
    if len(rows) == 0: return decision_node()
    current_score = entropy(rows)
    best_gain = 0.0
    best_criteria = None
    best_sets = None
    column_count = len(rows[0]) - 1
    labels = rows.T[len(rows[0]) - 1]
    for column_index in range(column_count):
        column_and_label = numpy.array([rows.T[column_index], labels.T]).T
        column_and_label = column_and_label[column_and_label[:,0].argsort()]
        counts_left = []
        counts_left.append(0)
        counts_left.append(0)
        counts_right = []
        counts_right.append(len(column_and_label) - numpy.count_nonzero(column_and_label.T[1]))
        counts_right.append(len(column_and_label) - counts_right[0])
        for i in range(len(column_and_label)):
            if i != 0 and column_and_label[i - 1][0] != column_and_label[i][0]:
                p = float(i)/len(column_and_label)
                gain = current_score - p * entropy_counts(counts_left) - (1 - p) * entropy_counts(counts_right)
                if gain > best_gain:# and i + 1 != len(column_and_label):
                    best_gain = gain
                    best_criteria = (column_index, column_and_label[i][0])
            if column_and_label[i][1] == 1:
                counts_left[1] += 1
                counts_right[1] -= 1
            else:
                counts_left[0] += 1
                counts_right[0] -= 1
    if best_gain > 0 and depth != 0:
        best_sets = divide_set(rows, best_criteria[0], best_criteria[1])
        true_node = build_weak_tree(best_sets[0], depth - 1)
        false_node = build_weak_tree(best_sets[1], depth - 1)
        return decision_node(col=best_criteria[0], value=best_criteria[1], true_node = true_node, false_node = false_node)
    else:
        return decision_node(result = unique_results(rows))

def error(weak_learner, D, rows):
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



if part4:
    print 'part 4: implementing adaboost'
    weak_learners, alphas = adaboost(training_data_and_labels, 500)
    print 'training data result'
    test_adaboost(training_data_and_labels, weak_learners, alphas)
    print 'testing data result'
    test_adaboost(test_data_and_labels, weak_learners, alphas)

def bagging(rows, num_trees):
    bag = set()
    num_data_points = int(0.7 * len(rows))
    for i in range(0, num_trees): # For each tree
        # First permute rows
        permuted_rows = numpy.random.permutation(rows)
        # Select 70% of permuted rows as training data for tree
        training_data = permuted_rows[0:num_data_points]
        tree = build_tree(training_data)
        bag.add(tree)
        print 'New tree in the bag'
    return bag

def test_bagging(bag, data, labels):
    test_forest(bag, data, labels)

if part5:
    print 'part 5: implementing bagging'
    bag = bagging(training_data_and_labels, 10)
    test_bagging(bag, test_data, test_labels)




def gini_impurity(rows):
    total = len(rows)
    results = unique_results(rows)
    impurity = 0
    for k1 in results.keys():
        p1 = float(results[k1])/total
        for k2 in results.keys():
            if k1 == k2: continue
            p2 = float(results[k2])/total
            impurity += p1*p2
    return impurity

def gini_impurity_counts(counts):
    impurity = 0
    if len(counts) == 0: return impurity
    p0 = float(counts[0]) / (counts[0] + counts[1])
    p1 = float(counts[1]) / (counts[0] + counts[1])
    impurity += 2*p0*p1
    return impurity




def build_tree_gini(rows):
    if len(rows) == 0: return decision_node()
    current_score = gini_impurity(rows)
    best_gain = 0.0
    best_criteria = None
    best_sets = None
    column_count = len(rows[0]) - 1
    labels = rows.T[len(rows[0]) - 1]
    for column_index in range(column_count):
        column_and_label = numpy.array([rows.T[column_index], labels.T]).T
        column_and_label = column_and_label[column_and_label[:,0].argsort()]
        counts_left = []
        counts_left.append(0)
        counts_left.append(0)
        counts_right = []
        counts_right.append(len(column_and_label) - numpy.count_nonzero(column_and_label.T[1]))
        counts_right.append(len(column_and_label) - counts_right[0])
        for i in range(len(column_and_label)):
            if i != 0 and column_and_label[i - 1][0] != column_and_label[i][0]:
                p = float(i)/len(column_and_label)
                gain = current_score - p * gini_impurity_counts(counts_left) - (1 - p) * gini_impurity_counts(counts_right)
                if gain > best_gain:# and i + 1 != len(column_and_label):
                    best_gain = gain
                    best_criteria = (column_index, column_and_label[i][0])
            if column_and_label[i][1] == 1:
                counts_left[1] += 1
                counts_right[1] -= 1
            else:
                counts_left[0] += 1
                counts_right[0] -= 1

    if best_gain > 0:
        best_sets = divide_set(rows, best_criteria[0], best_criteria[1])
        true_node = build_tree(best_sets[0])
        false_node = build_tree(best_sets[1])
        return decision_node(col=best_criteria[0], value=best_criteria[1], true_node = true_node, false_node = false_node)
    else:
        return decision_node(result = unique_results(rows))




if part6:
    print 'part 6: implementing gini impurity instead of entropy on decision tree'
    tree = build_tree_gini(training_data_and_labels)

    print 'Full tree with gini impurity'
    test_tree(tree, test_data, test_labels)






class quadrary_decision_node:
    def __init__(self, col=-1, value=None, false_false_node=None, true_true_node=None, true_false_node=None, false_true_node=None, result=None):
        self.col = col
        self.value = value
        self.result = result
        self.true_true_node = true_true_node
        self.false_false_node = false_false_node
        self.true_false_node = true_false_node
        self.false_true_node = false_true_node


def build_quad_tree(rows):
    if len(rows) == 0: return decision_node()
    current_score = entropy(rows)
    best_gain = [0.0, 0.0]
    best_criteria = [None, None]
    column_count = len(rows[0]) - 1
    labels = rows.T[len(rows[0]) - 1]
    for column_index in range(column_count):
        best_gain_column = 0.0
        best_criteria_column = None
        column_and_label = numpy.array([rows.T[column_index], labels.T]).T
        column_and_label = column_and_label[column_and_label[:,0].argsort()]
        counts_left = []
        counts_left.append(0)
        counts_left.append(0)
        counts_right = []
        counts_right.append(len(column_and_label) - numpy.count_nonzero(column_and_label.T[1]))
        counts_right.append(len(column_and_label) - counts_right[0])
        for i in range(len(column_and_label)):
            if i != 0 and column_and_label[i - 1][0] != column_and_label[i][0]:
                p = float(i)/len(column_and_label)
                gain = current_score - p * entropy_counts(counts_left) - (1 - p) * entropy_counts(counts_right)
                if gain > best_gain_column:# and i + 1 != len(column_and_label):
                    best_gain_column = gain
                    best_criteria_column = (column_index, column_and_label[i][0])
            if column_and_label[i][1] == 1:
                counts_left[1] += 1
                counts_right[1] -= 1
            else:
                counts_left[0] += 1
                counts_right[0] -= 1
        if best_gain_column > best_gain[1]:
            if best_gain_column > best_gain[0]:
                best_gain[1] = best_gain[0]
                best_gain[0] = best_gain_column
                best_criteria[1] = best_criteria[0]
                best_criteria[0] = best_criteria_column
            else:
                best_gain[1] = best_gain_column
                best_criteria[1] = best_criteria_column

    if best_gain[0] > 0 and best_gain[1] > 0:
        best_sets = divide_quad_set(rows, best_criteria[0][0], best_criteria[0][1], best_criteria[1][0], best_criteria[1][1])
        true_true_node = build_tree(best_sets[0])
        true_false_node = build_tree(best_sets[1])
        false_false_node = build_tree(best_sets[2])
        false_true_node = build_tree(best_sets[3])
        return quadrary_decision_node(col=(best_criteria[0][0], best_criteria[1][0]), value=(best_criteria[0][1], best_criteria[1][1]), true_true_node = true_true_node, false_false_node = false_false_node, true_false_node = true_false_node, false_true_node = false_true_node)
    elif best_gain[0] > 0:
        best_sets = divide_set(rows, best_criteria[0][0], best_criteria[0][1])
        true_node = build_tree(best_sets[0])
        false_node = build_tree(best_sets[1])
        return decision_node(col=best_criteria[0][0], value=best_criteria[0][1], true_node = true_node, false_node = false_node)
    else:
        return decision_node(result = unique_results(rows))

def divide_quad_set(rows, column_index1, value1, column_index2, value2):
    set1 = numpy.array([row for row in rows if row[column_index1] >= value1 and row[column_index2] >= value2])
    set2 = numpy.array([row for row in rows if row[column_index1] >= value1 and row[column_index2] < value2])
    set3 = numpy.array([row for row in rows if row[column_index1] < value1 and row[column_index2] < value2])
    set4 = numpy.array([row for row in rows if row[column_index1] < value1 and row[column_index2] >= value2])

    return (set1, set2, set3, set4)


def test_quad_tree(tree, data, labels):
    correct = 0
    for i in range(0, len(data)):
        d = data[i]
        result = predict_quad_tree(tree, d)
        if result == labels[i][0]:
            correct += 1
    print float(correct) / len(data)


def predict_quad_tree(tree, data):
    current_node = tree
    while current_node.result == None:
        if isinstance(current_node, decision_node):
            if data[current_node.col] >= current_node.value:
                current_node = current_node.true_node
            else:
                current_node = current_node.false_node
        else:
            if data[current_node.col[0]] >= current_node.value[0]:
                if data[current_node.col[1]] >= current_node.value[1]:
                    current_node = current_node.true_true_node
                else:
                    current_node = current_node.true_false_node
            else:
                if data[current_node.col[1]] >= current_node.value[1]:
                    current_node = current_node.false_true_node
                else:
                    current_node = current_node.false_false_node
    return majority_vote(current_node.result)


if part7:
    print 'part7: quad decision trees'
    quad_tree = build_quad_tree(training_data_and_labels)
    print 'Quad Tree'
    test_quad_tree(quad_tree, test_data, test_labels)


def test_cross_tree(tree, data):
    correct = 0
    for i in range(0, len(data)):
        d = data[i]
        result = predict_tree(tree, d)
        if result == data[i][57]:
            correct += 1
    return float(correct) / len(data)

def build_cross_tree(rows, k):
    num_data_points = int(0.7 * len(rows))
    num_validation_points = len(rows) - num_data_points
    best_accuracy = 0
    best_tree = None
    for i in range(0, k):
        # First permute rows
        rows = numpy.random.permutation(rows)
        #Select 90% of permuted rows as training data for tree
        training_data = rows[0:num_data_points]
        validation_data = rows[num_data_points:len(rows)]
        tree = build_tree(training_data)
        accuracy = test_cross_tree(tree, validation_data)
        if accuracy > best_accuracy:
            best_tree = tree
            best_accuracy = accuracy
    return best_tree

if part8:
    print 'part 8: Cross validation trees'
    tree = build_cross_tree(training_data_and_labels, 10) # 10-fold cross validation
    print 'Full tree'
    test_tree(tree, test_data, test_labels)
