import ystockquote
from datetime import datetime
import numpy


def convert_to_date_time(x):
    return datetime.strptime(x, '%Y-%m-%d')
vfunc_convert_to_date_time = numpy.vectorize(convert_to_date_time)


def good_day(opening_price, closing_price):
    if float(closing_price) > float(opening_price) * 1.015:
        return 1
    else:
        return 0

vfunc_good_day = numpy.vectorize(good_day)

def query_symbol(symbol):
    result = ystockquote.get_historical_prices(symbol, '19920101', '20130101')
    result = numpy.array(result)
    result = result[1:]
    dates = result.T[0]
    open_price = result.T[1]
    high_price = result.T[2]
    low_price = result.T[3]
    close_price = result.T[4]
    volume = result.T[5]
    adjusted_closing_price = result.T[6]
    dates = vfunc_convert_to_date_time(dates)
    good_days = vfunc_good_day(open_price, close_price)
    print 'Number of good days ', numpy.count_nonzero(good_days), 'out of ', len(good_days), 'days'
    to_store = numpy.column_stack([dates, good_days])
    f = open(symbol + '.npy', 'w')
    numpy.save(f, to_store)
    f.close()




query_symbol('AAPL')
