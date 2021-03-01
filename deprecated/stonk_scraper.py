from bs4 import BeautifulSoup
import requests
import re
import csv
import time
import random

def convert(text):
    returnVal = text
    try:
        if re.search("B", text):
            num = float(text.replace("B", ""))
            num = num * 10**9
            returnVal =  str(num)
        if re.search("M", text):
            num = float(text.replace("M", ""))
            num = num * 10**6
            returnVal =  str(num)
        if re.search("T", text):
            num = float(text.replace("T", ""))
            num = num * 10**12
            returnVal =  str(num)
        if re.search("k", text):
            num = float(text.replace("k", ""))
            num = num * 10**3
            returnVal = str(num)
    except ValueError:
        returnVal = text
    #print(returnVal)
    return returnVal


nyse_regex = re.compile("nyse")
nasdaq_regex = re.compile('nasdaq')

wiki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
page = requests.get(wiki_url)
soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find_all('table')[0]
companies = table.find_all('tr')
companies_list = []
headers = ["Code", "Debt to Equity"]
i = 0
for i in range(0, 506):
    if i == 0:
        continue
    company_data = []
    company = companies[i]
    code = company.find_all('a', {'class', 'external text'})[0].get_text()
    company_data.append(code)
    print(code)
    try:
        if(i % 20 == 0):
            time.sleep(random.randint(1, 5))
        elif i % 50 == 0:
            time.sleep(random.randint(15, 30))
        else:
            time.sleep(random.randint(1, 5) * .05)

        yahoo_url = "https://finance.yahoo.com/quote/"+code+"/key-statistics"

        yahoo_page = requests.get(yahoo_url)

        yahoo_soup = BeautifulSoup(yahoo_page.content, 'html.parser')
        tables = yahoo_soup.find_all('table')

        first_table = tables[0].find_all('tr')
        market_cap = convert(first_table[1].find_all('td')[1].get_text())

        pe_ratio = first_table[3].find_all('td')[1].get_text()
        #company_data.append(pe_ratio)

        #price_to_sales = first_table[6].find_all('td')[1].get_text()
        #company_data.append(price_to_sales)

        ninth_table = tables[9].find_all('tr')
        free_cash_flow = convert(ninth_table[1].find_all('td')[1].get_text())
        free_cash_flow_ratio = -1
        if free_cash_flow != 'N/A' and market_cap != 'N/A':
            free_cash_flow_ratio = round(float(free_cash_flow) / float(market_cap) * 100, 2)

        #company_data.append(free_cash_flow_ratio)

        price_to_book = first_table[7].find_all('td')[1].get_text()
        #company_data.append(price_to_book)

        #contains beta
        second_table = tables[1].find_all('tr')

        #beta = second_table[0].find_all('td')[1].get_text()
        #company_data.append(beta)

        sixth_table = tables[6].find_all('tr')
        #return_on_equity = sixth_table[1].find_all('td')[1].get_text().replace("%", "")
       # company_data.append(return_on_equity)

        eighth_table = tables[8].find_all('tr')
        debt_to_equity = eighth_table[3].find_all('td')[1].get_text()
        company_data.append(debt_to_equity)

        third_table = tables[3].find_all('tr')
       # payout_ratio = third_table[5].find_all('td')[1].get_text().replace("%", "")
        #company_data.append(payout_ratio)



        print(company_data)
        companies_list.append(company_data)

        with open('s&p500Stonks.csv', 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            if i == 0:
                writer.writerow(headers)
                i+=1
            else:
                writer.writerow(company_data)
    except IndexError:
        print(code + " had a format error, not using")















