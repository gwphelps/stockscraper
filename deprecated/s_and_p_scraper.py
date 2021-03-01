from bs4 import BeautifulSoup
import requests
import csv

def appendToCSV(codeVar, nameVar, industryVar):
    with open('../s&p500_name_code.csv', 'a', newline="\n") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow([codeVar, nameVar, industryVar])



wiki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
page = requests.get(wiki_url)
soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find_all('table')[0]
companies = table.find_all('tr')
companies_list = []
headers = []
tickerString = ""




with open('../s&p500_name_code.csv', 'w', newline="\n") as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    row = ['code', 'name', 'industry']
    writer.writerow(row)
for i in range(0, 506):
    if i == 0:
        continue
    company_data = []
    company = companies[i]
    code = company.find_all('a', {'class', 'external text'})[0].get_text()
    name = (company.find_all('a')[1]
        .get_text()
        .lower()
        .replace(".com", "")
        .replace(".", "")
        .replace("svcgp", "")
        .replace("\"", "")
        .replace("\'", "")
        .replace(",", "")
        .replace(" ltd", "")
        .replace(" &", "")
        .replace(" company", "")
        .replace(" laboratories", "")
        .replace(" inc", "")
        .replace(" corporation", "")
        .replace(" corp", "")
        .replace(" co", "")
        .replace(" plc", "")
        .replace(" ", "-"))
    industry = company.find_all('td')[3].get_text()
    appendToCSV(code, name, industry)
