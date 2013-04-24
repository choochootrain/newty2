import ystockquote
from datetime import datetime
import numpy
import sys
import json
f = open(sys.argv[1]+'.npy', 'r')
dates_and_good_days = numpy.load(f)
to_write = open(sys.argv[1] + '.json', 'w')
dates_and_good_days_array = []
for date, good_day in dates_and_good_days:
    dates_and_good_days_array.append([date.strftime('%m/%d/%Y'), good_day])

to_write.write(json.dumps(dates_and_good_days_array))
f.close()
to_write.close()
