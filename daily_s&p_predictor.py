import pandas, math
from statistics import mean
import csv
import top_20_filter
for yearRange in range(5, 6):
    equations_df = pandas.read_csv('yearlys&p/'+str(yearRange)+'_year_s&p500_industry_equations.csv')
    equations_df.set_index('industry', inplace=True, drop=True)
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
    stocks_df = pandas.read_csv('s&p500_daily_stats_adjusted.csv')
    for i in range(len(stocks_df)):
        try:
            stock = stocks_df.loc[i]
            #print(stock)
            if stock['code'] == 'VZ':
                continue
            industry = stock['industry']
            pe_c = equations_df.loc[industry]['pe_c']
            fcf_c = equations_df.loc[industry]['fcf_c']
            pb_c = equations_df.loc[industry]['pb_c']
            ps_c = equations_df.loc[industry]['ps_c']
            intercept = equations_df.loc[industry]['intercept']
            #print(stock)
            prediction = round(
                pe_c * stock['pe-ratio']
                + fcf_c * stock['price-fcf']
                + pb_c * stock['price-book']
                + pb_c * stock['price-sales']
                + intercept, 2)
            #actual = stock['stockratio']
            predictionData = {
                'stock': stock['code'],
                'industry': industry,
                'pe-ratio': round(stock['pe-ratio'], 2),
                'price-fcf': round(stock['price-fcf'], 2),
                'price-book': round(stock['price-book'], 2),
                'price-sales': round(stock['price-sales'], 2),
                'prediction': prediction
            }
            predictions.append(predictionData)
            #print(predictionData)
        except KeyError and ValueError:
            continue


    predictions.sort(key= lambda i: float(i['prediction']), reverse=True)
    top10_predict = predictions
    #print(top10_predict)

    chosen_stocks = [
        'GOOG',
        'TMUS',
        'ATVI',
        'FIS',
        'ALK',
        'APTV',
        'ADSK',
        'AVY',
        'BLL',
        'AMGN'
    ]
    bads = []
    chosen_predictions= []
    for stock in top10_predict:
        if math.isinf(stock['prediction']) or stock['prediction'] == 'nan' or math.isnan(stock['prediction']):
            #print("found bad")
            bads.append(stock)
        elif stock['pe-ratio'] == 0 or stock['price-fcf'] == 0 or stock['price-book'] == 0 or stock['price-sales'] == 0:
            bads.append(stock)
        if stock['stock'] in chosen_stocks:
            chosen_predictions.append(stock)

    for bad in bads:
        top10_predict.remove(bad)
    top10_predict.sort(key= lambda i: float(i['prediction']), reverse=True)
    overall_market_growth = round(mean(d['prediction'] for d in top10_predict), 2)

    found_industries = []
    for prediction in top10_predict:
        industry = prediction['industry']
        if len(industries[industry]) < 3:
            industries[industry].append(prediction)
    for industry in industries.keys():
        found_industries = found_industries + industries[industry]

    top10_predict = sorted(found_industries, key=lambda i: i['prediction'], reverse=True)



    #print(top10_predict)

    avg_growth_top_10 = round(mean(d['prediction'] for d in top10_predict[0:10]), 2)



    print("top 10 overall: ")
    with open(str(yearRange)+'_year_predictions.csv', 'w', newline="\n") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['code', 'industry', 'pe-ratio', 'price-fcf', 'price-book','price-sales', 'prediction'])
    for stock in top10_predict[:20]:
        #print(stock)
        with open(str(yearRange)+'_year_predictions.csv', 'a', newline="\n") as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(stock.values())
    print("projected growth: "+str(avg_growth_top_10))
    print("overall s&p growth prediction: "+str(overall_market_growth))