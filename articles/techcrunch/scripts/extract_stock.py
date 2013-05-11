import csv
file = "aapl_stock.csv"
reader = csv.reader(open(file),delimiter=',')
reader.next()

data = []
last = 0
mp = 0
mmp = 10000000
mc = 0
mmc = 10000000
for row in reader:
  date = row[0] + 'T00:00:00';
  price = float(row[6])
  change = price - last
  mp = max(mp, price)
  mc = max(mc, change)
  mmp = min(mmp, price)
  mmc = min(mmc, change)
  data.append({'date':date, 'price':price, 'change':change})

  last = price
print data
print mmp, mp
print mmc, mc
