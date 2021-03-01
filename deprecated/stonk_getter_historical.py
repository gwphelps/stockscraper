import yfinance as yf
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import csv


def formatData(values, headers):
    row = []

    for header in headers:
        if header == 'longBusinessSummary':
            row.append('N/A')
            continue
        try:
            stat = values[header]
            row.append(stat)
        except KeyError:
            row.append("N/A")
        except ValueError:
            row.append("N/A")
    #print(row)
    return row


wiki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
page = requests.get(wiki_url)
soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find_all('table')[0]
companies = table.find_all('tr')
companies_list = []
headers = []
tickerString = ""
for i in range(0, 506):
    if i == 0:
        continue
    company_data = []
    company = companies[i]
    code = company.find_all('a', {'class', 'external text'})[0].get_text()
    tickerString += " " + code

tickers = yf.download("MMM", start="2015-01-01", end="2019-12-31")
print(tickers)
i = 0
for index in range(0, len(tickers.tickers)):
    try:
        ticker = tickers.tickers[index]
        info = ticker.history(period="max")
        print(info["Dividends"])
        #for day in info['Stock Splits']:
            #print(day)
        if i == 0:
            #writeFunc(info.keys())
            headers = info.keys()
            i+=1
        csvRow = formatData(info, headers)
        #writeFunc(csvRow)
    except ValueError:
        print("skip,  value error")
    except KeyError:
        print("skip, key error")




