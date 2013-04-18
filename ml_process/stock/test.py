f = open('AAPL.npy', 'r')
import numpy
x = numpy.load(f)
print x
print 'one_result', x[0]
