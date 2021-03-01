import csv
import sys
companies = []
top_companies = {}
def sort(stat, minValue, sortIndex):
    if minValue == -1:
        return True
    elif(sortLow[sortIndex]):
        return stat < minValue
    else:
        return stat > minValue


    stat < minValue or minValue == -1
sortLow = [True, True, True, True, True, True, False, False]
with open('s&p500Stonks.csv', newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    i = 0
    headers = []
    for row in reader:
        if i == 0:
            headers = row
            i+=1
            continue
        companies.append(row)
    for index in range(1, len(headers)):
        header = headers[index]
        print("top 10 " + header)

        top10 = {}
        for num in range(0, 50):
            minValue = -1
            minName = ""
            for company in companies:
                if company[index] == 'N/A' or company[index] == '-1':
                    continue
                stat = float(company[index].replace('k', '').replace(",", ""))
                if sort(stat, minValue, index-1):
                    try:
                        top10[company[0]]
                    except KeyError:
                        minValue = stat
                        minName = company[0]
            top10[minName] = minValue
        print(top10)
        if index != len(headers)-1:
            for key in top10.keys():
                try:
                    top_companies[key] += 1
                except KeyError:
                    top_companies[key] = 1
    for key in top_companies.keys():
        if top_companies[key] >= 3:
            print(key + " : " + str(top_companies[key]))










