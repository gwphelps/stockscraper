import csv
import re
import pandas
from statistics import mean
RANGE = 1 #years





average_df = pandas.read_csv('industry_averages/s&p500_growth_by_year.csv')
average_df.set_index('year', inplace=True, drop=True)

def averageReturn(startyear, endyear):
    print(startyear)

    market_change = 1
    for year in range(startyear, endyear):
        percent_change = average_df.loc[year]['annual_change']
        market_change *= (1 + (percent_change / 100))
    return market_change

def calculateMetricRatio(metricValue, metricName, startyear):
    if metricValue == 0.0:
        print("USING AVERAGE")
        return 1
    return float(metricValue) / average_df.at[startyear, metricName]

def calculateHistoricalData(company_code, month, startyear, endyear):
    print(month)
    returnRow = []
    fileName = 'historical/s&p500_historical_' + company_code + '.csv'
    with open(fileName, newline='\n') as csvhistfile:
        histreader = csv.reader(csvhistfile, delimiter=',')
        startPrice = 0
        endPrice = 0
        startPE = 0
        startFCF = 0
        startPB = 0
        startPS = 0
        pattern_start = re.compile(str(startyear-1) + '-'+str(month)+'-\d\d')
        found_start = False
        pattern_end = re.compile(str(endyear-1) + '-'+str(month)+'-\d\d')
        found_end = False
        for histrow in histreader:
            if re.match(pattern_start, histrow[0]) and not found_start:
                print(histrow[0])
                startPrice = histrow[1]
                startPE = histrow[2]
                startFCF = histrow[3]
                startPB = histrow[4]
                startPS = histrow[5]
                found_start = True
            if re.match(pattern_end, histrow[0]) and not found_end:
                print(histrow[0])
                endPrice = histrow[1]
                found_end = True
        try:
            priceratio = float(endPrice) / float(startPrice)
            print(priceratio)
            #normalize by the overall change in s&p500 in given 5 year stretch
            priceratio_normalized = (priceratio / averageReturn(startyear, endyear))*100
            if priceratio == 0:
                return None
            print(priceratio_normalized)
            returnRow.append(priceratio_normalized)
        except ZeroDivisionError:
            return None
        returnRow.append(calculateMetricRatio(startPE, 'initialPE', startyear))
        returnRow.append(calculateMetricRatio(startFCF, 'initialFCF', startyear))
        returnRow.append(calculateMetricRatio(startPB, 'initialPB', startyear))
        returnRow.append(calculateMetricRatio(startPS, 'initialPS', startyear))
        return returnRow

def sendToOutput(peData):
    with open('yearlys&p/'+str(RANGE)+'_year_s&p500_pe_stock_ratio.csv', 'a', newline='\n') as outputAppendCsv:
        outputWriter = csv.writer(outputAppendCsv, delimiter=",")
        outputWriter.writerow(peData)
for yearRange in range(5, 6):
    RANGE = yearRange
    with open('yearlys&p/'+str(RANGE)+'_year_s&p500_pe_stock_ratio.csv', 'w', newline='\n') as outputCsv:
        writer = csv.writer(outputCsv, delimiter=",")
        writer.writerow(['code', 'industry', 'stockratio', 'initialPE', 'initialFCF', 'initialPB', 'initialPS'])
    for yearConst in range(2007, 2021-RANGE):
        with open('s&p500_name_code.csv', newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            i = 0

            for row in reader:
                if i == 0:
                    i +=1
                    continue
                code = row[0]
                print(code)

                for month in ['1[0-2]']:#['0[1-3]', '0[4-6]', '0[7-9]', '1[0-2]']:
                    data = []
                    data.append(code)
                    data.append(row[2])
                    histData = calculateHistoricalData(code, month, yearConst, yearConst + RANGE)
                    if histData == None:
                        print("skip due to not correct data")
                        continue

                    data.append(float(histData[0]))
                    data.append(histData[1])
                    data.append(histData[2])
                    data.append(histData[3])
                    data.append(histData[4])
                    print(data)
                    sendToOutput(data)



