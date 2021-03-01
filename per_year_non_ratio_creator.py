import csv
import re
import pandas
from statistics import mean
RANGE = 5 #years



average_df = pandas.read_csv('s&p500_growth_by_year.csv')
average_df.set_index('year', inplace=True, drop=True)


def averageReturn(startyear, endyear):
    print(startyear)

    market_change = 1
    for year in range(startyear, endyear):
        percent_change = average_df.loc[year]['annual_change']
        market_change *= (1 + (percent_change / 100))
    return market_change


def calculateHistoricalData(company_code, startyear, endyear):
    returnRow = []
    fileName = 'historical/s&p500_historical_' + company_code + '.csv'
    with open(fileName, newline='\n') as csvhistfile:
        previousPrice = 0
        histreader = csv.reader(csvhistfile, delimiter=',')
        startPrice = 0
        endPrice = 0
        startPE = 0
        startFCF = 0
        startPB = 0
        startPS = 0
        #pattern_year_before = re.compile(str(startyear-1) + '-1[0-2]-\d\d')
        #found_year_before = False
        pattern_start = re.compile(str(startyear-1) + '-1[0-2]-\d\d')
        found_start = False
        pattern_end = re.compile(str(endyear-1) + '-1[0-2]-\d\d')
        found_end = False
        for histrow in histreader:
            #if re.match(pattern_year_before, histrow[0]) and not found_year_before:
            #    previousPrice = histrow[1]

            if re.match(pattern_start, histrow[0]) and not found_start:
                print(histrow[0])
                startPrice = histrow[1]
                startPE = histrow[2]
                startFCF = histrow[3]
                startPB = histrow[4]
                startPS = histrow[5]
                #print(histrow)
                found_start = True
            if re.match(pattern_end, histrow[0]) and not found_end:
                print(histrow[0])
                endPrice = histrow[1]
                found_end = True
        try:
            priceratio = (float(endPrice) / float(startPrice))
            print(priceratio)
            #previousRatio = ((float(startPrice) / float(previousPrice)) / averageReturn(startyear, endyear))*100
            #normalize by the overall change in s&p500 in given 5 year stretch
            priceratio_normalized = (priceratio / averageReturn(startyear, endyear))*100
            if priceratio == 0:
                return None
            print(priceratio_normalized)
            returnRow.append(priceratio_normalized)
            #returnRow.append(previousRatio)
        except ZeroDivisionError:
            return None

        returnRow.append(float(startPE))#/average_df.at[startyear, 'initialPE'])
        returnRow.append(float(startFCF))#/average_df.at[startyear, 'initialFCF'])
        returnRow.append(float(startPB))#/average_df.at[startyear, 'initialPB'])
        returnRow.append(float(startPS))#/average_df.at[startyear, 'initialPS'])
        print(returnRow)
        return returnRow

def sendToOutput(peData):
    with open('yearlys&p/'+str(RANGE)+'_year/s&p500_pe_stock_nonratio_'+str(yearConst)+'.csv', 'a', newline='\n') as outputAppendCsv:
        outputWriter = csv.writer(outputAppendCsv, delimiter=",")
        outputWriter.writerow(peData)

for rangeConst in range(1, 6):
    RANGE = rangeConst
    for yearConst in range(2007, 2022-RANGE):
        with open('s&p500_name_code.csv', newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            i = 0
            with open('yearlys&p/'+str(RANGE)+'_year/s&p500_pe_stock_nonratio_'+str(yearConst)+'.csv', 'w', newline='\n') as outputCsv:
                writer = csv.writer(outputCsv, delimiter=",")
                writer.writerow(['code', 'industry', 'stockratio', 'initialPE', 'initialFCF', 'initialPB', 'initialPS'])
            for row in reader:
                if i == 0:
                    i +=1
                    continue
                code = row[0]
                print(code)

                for year in range(yearConst, yearConst+1):
                    data = []
                    data.append(code)
                    data.append(row[2])
                    histData = calculateHistoricalData(code, year, year + RANGE)
                    if histData == None:
                        print("skip due to not correct data")
                        continue

                    data.append(float(histData[0]))
                    data.append(histData[1])
                    data.append(histData[2])
                    data.append(histData[3])
                    data.append(histData[4])
                    #data.append(histData[5])
                    print(data)
                    sendToOutput(data)




