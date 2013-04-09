import numpy
import scipy
import scipy.cluster.hiearchy as hcluster
import numpy.random as random
import pylab
import json
f = open('clean_body_word_counts.json', 'r')
labels = []
dataset = []
for line in f:
    line_arr = json.loads(line)
    labels.append(line[0])
    dataset.append(line[1])



from hcluster import *


Y=pdist(X, 'seuclidean')
Z=linkage(Y, 'single')
dendrogram(Z, color_threshold=0)
