from bs4 import BeautifulSoup
import requests
import csv
import pandas, math
import re
from statistics import mean


metrics = ['pe-ratio', 'price-fcf', 'price-book', 'price-sales']

def getStockPrice(code, name):
    url = "https://www.macrotrends.net/stocks/charts/" + code + "/" + name + "/pe-ratio"
    page = requests.get(url)
    if (page.status_code == 404):
        return None
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table')[0].find_all('tr')

    return table[2].find_all('td')[1].get_text()
def getMetricValue(code, name, metric):
    url = "https://www.macrotrends.net/stocks/charts/" + code + "/" + name + "/" + metric
    page = requests.get(url)
    if (page.status_code == 404):
        return None
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find_all('table')[0].find_all('tr')

    return float(table[2].find_all('td')[3].get_text())



stock_data = {
    'code': [],
    'industry': [],
    'price': [],
    'pe-ratio': [],
    'price-fcf': [],
    'price-book': [],
    'price-sales': []
}
with open('s&p500_name_code.csv', newline="\n") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    i = 0
    for row in reader:
        if i == 0:
            i+=1
            continue

        code = row[0]
        print(code)
        name = row[1]
        industry = row[2]
        stock_data['code'].append(code)
        stock_data['price'].append(getStockPrice(code, name))
        stock_data['industry'].append(industry)
        for metric in metrics:
            value = getMetricValue(code, name, metric)
            print(value)
            if math.isinf(value):
                stock_data[metric].append(math.nan)
            else:
                stock_data[metric].append(value)

        print('\n')

    pandas.DataFrame(stock_data).to_csv('s&p500_daily_stats.csv')




