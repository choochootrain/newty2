import numpy
import sys
from pylab import *
if len(sys.argv) < 2:
    print 'need symbol as first command line argument'
    sys.exit(0)

symbol = sys.argv[1]
f = open(symbol + '.npy', 'r')
x = numpy.load(f)

dates = x.T[0]
good_days = x.T[1]
figure(figsize=(100, 20))
plot(dates, good_days, linewidth=0.0, marker='.')

ylim([-.5, 1.5])
title(symbol + ' Good Days')
xlabel('dates')
ylabel('good days')
savefig(symbol + '_good_days.png', dpi=100)
