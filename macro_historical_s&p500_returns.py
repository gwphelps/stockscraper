from bs4 import BeautifulSoup
import requests
import csv

with open('s&p500_growth_by_year.csv', 'w', newline="\n") as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    page = requests.get('https://www.macrotrends.net/2526/sp-500-historical-annual-returns')
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table')[0].find_all('tr')

    year = 0
    annual_change = 0
    writer.writerow(['year', 'annual_change'])
    for i in range(2, len(table)):
        row = table[i].find_all('td')
        year = row[0].get_text()
        annual_change = row[6].get_text().replace("%", "")
        writer.writerow([year, annual_change])

