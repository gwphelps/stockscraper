from bs4 import BeautifulSoup
import requests
import csv


metrics = ['pe-ratio', 'price-fcf', 'price-book', 'price-sales']

def getMetricValue(code, name, metric):
    tableArr = []
    url = "https://www.macrotrends.net/stocks/charts/" + code + "/" + name + "/" + metric
    page = requests.get(url)
    if (page.status_code == 404):
        return None
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find_all('table')[0].find_all('tr')

    headers = []
    headerSoup = table[1].find_all('th')
    for headerIndex in range(len(headerSoup)):
        if headerIndex == 2:
            continue
        headers.append(headerSoup[headerIndex].get_text())

    tableArr = []
    tableArr.append(headers)

    with open('historical/s&p500_historical_' + code + '.csv', 'w', newline="\n") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(headers)
    for tableIndex in range(2, len(table)):
        tableRow = table[tableIndex].find_all('td')
        rowArr = []

        for colIndex in range(4):
            if(colIndex == 2):
                continue
            rowArr.append(tableRow[colIndex].get_text().replace("\n", ""))

        tableArr.append(rowArr)
    return tableArr

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
        tables = {}
        stockPriceGrabbed = False
        for metric in metrics:
            metricTable = getMetricValue(code, name, metric)

            for metricRow in metricTable:
                #print(metricRow)
                #stock price is only grabbed once
                for metricIndex in range(1, len(metricRow)):
                    #if metricIndex == 1:
                        #if stockPriceGrabbed:
                            #continue
                        #stockPriceGrabbed = True

                    try:
                        tables[metricRow[0]].append(metricRow[metricIndex])
                    except KeyError:
                        tables[metricRow[0]] = []
                        tables[metricRow[0]].append(metricRow[metricIndex])




        finalTableArr = []
        for key in tables.keys():
            row = tables[key]
            writeType = 'a'
            if key == 'Date':
                writeType = 'w'
            tableRow = tables[key]
            try:
                tableRow.pop(2)
                tableRow.pop(3)
                tableRow.pop(4)
            except IndexError:
                continue
            tableRow.insert(0, key)

            print(tableRow)
            with open('historical/s&p500_historical_' + code + '.csv', writeType, newline="\n") as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                writer.writerow(tableRow)









