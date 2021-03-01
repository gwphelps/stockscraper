import csv, statistics

for yearRange in range(1, 6):
    stocks = []
    with open('yearlys&p/'+str(yearRange)+'_year_s&p500_pe_stock_ratio.csv', newline="\n") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            stocks.append({
                'code': row[0],
                'industry': row[1],
                'stockratio': row[2],
                'initialPE': row[3],
                'initialFCF': row[4],
                'initialPB': row[5],
                'initialPS': row[6]
            })
        stocks = sorted(stocks, key=lambda i: i['initialPE'], reverse=True)[10:]
        stocks = sorted(stocks, key=lambda i: i['initialFCF'], reverse=True)[10:]
        stocks = sorted(stocks, key=lambda i: i['initialPB'], reverse=True)[10:]
        stocks = sorted(stocks, key=lambda i: i['initialPS'], reverse=True)[10:]
        stocks = sorted(stocks, key=lambda i: i['initialPB'], reverse=False)[10:]
    with open('yearlys&p/'+str(yearRange)+'_year_s&p500_pe_stock_ratio.csv', 'w', newline="\n") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['code',
                'industry',
                'stockratio',
                'initialPE',
                'initialFCF',
                'initialPB',
                'initialPS'])
        for stock in stocks:
            writer.writerow(stock.values())