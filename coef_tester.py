import csv

import pandas, random
from statistics import mean
import sys, re
import top_20_filter
import method_tester



#print(equations_df)
#stocks_df = pandas.read_csv('s&p500_pe_stock_ratio.csv')
best_out_of_guesses = []
def calculateRankError(predictRanks, actualRanks):
    predictRankTotal = 0
    actualRankTotal = 0
    try:
        rankingsString = "predictedRanks: ["
        for i in range(0, 10):
            stock = predictRanks[i]
            j = actualRanks.index(stock)
            predictRankTotal += i+1
            actualRankTotal += j + 1
            rankingsString += "("+str(i)+","+str(j)+")"
        rankingsString+="]"
        print(rankingsString)
    except:
        print("AAAHHH BAD RANK SOMEHOW")
        return total_rank_error/num
    return round(((actualRankTotal/10)-(predictRankTotal/10))/(predictRankTotal/10), 2)


predictionListByN = {
    1: {},
    2: {},
    3: {},
    4: {},
    5: {}
}
one_year_actuals = {}
total_rank_error = 0
num = 0
total_unused_errors = 0
for iRange in range(5, 6):
    total_unused_errors = 0
    print(str(iRange)+" YEAR INCREMENTS\n--------------------")
    equations_df = pandas.read_csv('yearlys&p/'+str(iRange)+'_year_s&p500_industry_equations.csv')
    equations_df.set_index('industry', inplace=True, drop=True)
    overall_growth = 0
    my_growth = 0
    my_growth_top10 = 0
    my_expected_growth_top10 = 0
    total_rank_error = 0
    num = 0
    for year in range(2007, 2021-iRange):
        industries = dict.fromkeys([
            'Information Technology',
            'Industrials',
            'Health Care',
            'Financials',
            'Communication Services',
            'Consumer Discretionary',
            'Materials', 'Utilities',
            'Real Estate',
            'Consumer Staples',
            'Energy'
        ])
        for industry in industries.keys():
            industries[industry] = []
        predictions = []
        print("\n"+str(year))
        stocks_df = pandas.read_csv('yearlys&p/'+str(iRange)+'_year/s&p500_pe_stock_ratio_'+str(year)+'.csv')
        for i in range(len(stocks_df)):
            try:
                stock = stocks_df.loc[i]

                if stock['code'] == 'VZ':
                    continue
                industry = stock['industry']
                pe_c = equations_df.loc[industry]['pe_c']
                fcf_c = equations_df.loc[industry]['fcf_c']
                pb_c = equations_df.loc[industry]['pb_c']
                ps_c = equations_df.loc[industry]['ps_c']
                intercept = equations_df.loc[industry]['intercept']

                prediction = round(
                    pe_c * stock['initialPE']
                    + fcf_c * stock['initialFCF']
                    + pb_c * stock['initialPB']
                    + ps_c + stock['initialPS']
                    + intercept, 2)
                actual = stock['stockratio']
                predictionData = {'stock': stock['code'], 'initialPE': stock['initialPE'], 'initialFCF': stock['initialFCF'], 'initialPB': stock['initialPB'], 'initialPS': stock['initialPS'], 'industry': stock['industry'], 'prediction': prediction, 'actual': actual}
                predictions.append(predictionData)

                #print(predictionData)
            except KeyError and ValueError:
                continue
        if iRange == 1:
            one_year_actuals[year] = predictions
        found_industries = []


        top10_predict = sorted(predictions, key=lambda i: i['prediction'], reverse=True)
        for prediction in top10_predict:
            industry = prediction['industry']
            if len(industries[industry]) < 3:
                industries[industry].append(prediction)
        for industry in industries.keys():
            found_industries = found_industries + industries[industry]

        top10_predict = sorted(found_industries, key=lambda i: i['prediction'], reverse=True)
        top_10_actual = sorted(predictions, key=lambda i: i['actual'], reverse=True)
        top10_overall = top_20_filter.reduce_to_10(top10_predict[0:20])
        for thing in top10_overall:
            print(thing)
        best_rows = sorted(top10_predict[0:20], key=lambda i: i['actual'], reverse=False)[0:5]
        if len(best_out_of_guesses) == 0:
            best_out_of_guesses.append(best_rows[0].keys())
        for best_row in best_rows:
            best_out_of_guesses.append(best_row.values())
        predictionListByN[iRange][year] = top10_overall

        overall_actual_growth = round(mean(d['actual'] for d in predictions), 2)
        overall_growth += overall_actual_growth

        average_predicted_growth_top10 = round(mean(d['prediction'] for d in top10_overall), 2)
        average_actual_growth_top10 = round(mean(d['actual'] for d in top10_overall), 2)
        my_growth_top10 += average_actual_growth_top10
        my_expected_growth_top10 += average_predicted_growth_top10
        num += 1
       # print("1 per industry selection:")

       # print("predicted growth: "+str(average_predicted_growth))
        #print('actual growth: '+str(average_actual_growth))

        print("top 10 selection:")
        print("predicted growth: " + str(average_predicted_growth_top10))
        print('actual growth: ' + str(average_actual_growth_top10))
        rank_error = calculateRankError(top10_overall, top_10_actual)
        #check_index = int(round(rank_error, 0))
        #median_stock = mean(d['actual'] for d in top_10_actual[check_index:check_index+10])
        #print(str(check_index) + "-"+str(check_index+10)+" stock: "+str(median_stock))
        total_rank_error += rank_error
        #print("% error: "+ str(rank_error) +"%")
        #print("top 10 actual:")
        #print(top_10_actual[0:9])
        #print(round(mean(d['actual'] for d in top_10_actual[0:9]), 2))

        print("overall selection")
        print("actual growth: "+str(overall_actual_growth))
    print("\ntotal average "+str(iRange)+" year growth from 2006-2019")
    my_avg = round(my_growth / num, 2)
    my_avg_top10 = round(my_growth_top10/ num, 2)
    overall_avg = round(overall_growth / num, 2)
    predicted_avg = round(my_expected_growth_top10 / num, 2)
    avg_error = round(total_rank_error / num, 2)
    #print("my growth 1 per industry: "+str(my_avg))
    print('my predicted growth: '+str(predicted_avg))
    print("my growth using top 10: "+str(my_avg_top10))
    print("%error: "+str(avg_error) + "%")
    print("overall growth: "+str(overall_avg))

#comparing different strategies
print("COMPARING DIFFERENT PREDICTION FORCASTS\n--------------------")
#print(predictionListByN)

#method_tester.five_year_hold(predictionListByN, one_year_actuals)

with open('worst_guesses.csv', 'w', newline="\n") as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for row in best_out_of_guesses:
        writer.writerow(row)




