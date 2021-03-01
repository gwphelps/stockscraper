from statistics import mean

#using n year predictions and only shuffling every n years
def n_year_shuffle(predictionListByN, one_year_actuals):
    growth_per_pred_type = []
    for n in range(1, 6):
        growth_per_start_year = []

        for startYear in range(2007, 2021-5):

            total_growth = 1
            pred_year = startYear
            for year in range(startYear, startYear + 5):
                if (year-startYear) % n == 0:
                    pred_year = year
                #print("pred_year: "+str(pred_year))
                #print(str(n)+" " +str(year))
                if year >= 2021-n:
                    continue
                predictions = predictionListByN[n][pred_year]
                growth_per_prediction = []
                #print(startYear)

                for prediction in predictions:
                    code = prediction['stock']
                    #print(prediction)
                    #print(year)
                    one_year_data = one_year_actuals[year]


                    growth_multiple_list = [d['actual'] for d in one_year_data if d['stock'] == code]
                    if len(growth_multiple_list) == 0:
                        continue
                    growth_multiple = float(growth_multiple_list[0])/100
                    growth_per_prediction.append(growth_multiple)
                    #total_growth *= growth_multiple
                total_growth *= mean(growth_per_prediction)
                #print(total_growth)
                #if total_growth != 1:
            growth_per_start_year.append(total_growth*100)
        print(growth_per_start_year)
        growth_per_pred_type.append({'n': n, 'value': mean(growth_per_start_year)})
    print("rebalancing 10 stocks every n years using n year prediction")
    print(growth_per_pred_type)

def one_year_shuffle(predictionListByN, one_year_actuals):
    # using n year predictions and shuffling every 1 year
    growth_per_pred_type = []
    for n in range(1, 6):
        growth_per_start_year = []

        for startYear in range(2007, 2021 - 5):

            total_growth = 1
            for year in range(startYear, startYear + 5):

                # print(str(n)+" " +str(year))
                if year >= 2021 - n:
                    continue
                predictions = predictionListByN[n][year]
                growth_per_prediction = []
                # print(startYear)

                for prediction in predictions:
                    code = prediction['stock']
                    # print(prediction)
                    # print(year)
                    one_year_data = one_year_actuals[year]

                    growth_multiple_list = [d['actual'] for d in one_year_data if d['stock'] == code]
                    if len(growth_multiple_list) == 0:
                        continue
                    growth_multiple = float(growth_multiple_list[0]) / 100
                    growth_per_prediction.append(growth_multiple)
                    # total_growth *= growth_multiple
                total_growth *= mean(growth_per_prediction)
                # print(total_growth)
                # if total_growth != 1:
            growth_per_start_year.append(total_growth * 100)
        print(growth_per_start_year)
        growth_per_pred_type.append({'n': n, 'value': mean(growth_per_start_year)})
    print("rebalancing 10 stocks every year based on n year predictions from that year")
    print(growth_per_pred_type)
    print(
        "conclusion, 3 year worked best for re-shuffling every year, which makes sense to me, since it's between one and 5 year predictions,"
        "not as good as just using the 5 year prediction though")
def five_year_hold(predictionListByN, one_year_actuals):
    # using 1 year growth prediction every year for 5 years
    growth_per_pred_type = []
    for n in range(1, 6):
        growth_per_start_year = []
        for startYear in range(2007, 2021 - 5):

            predictions = predictionListByN[n][startYear]
            growth_per_prediction = []
            for prediction in predictions:
                total_growth = 1
                # print(prediction)
                code = prediction['stock']

                # print(startYear)
                for year in range(startYear, startYear + 5):
                    # print(year)
                    one_year_data = one_year_actuals[year]

                    growth_multiple_list = [d['actual'] for d in one_year_data if d['stock'] == code]
                    if len(growth_multiple_list) == 0:
                        continue
                    growth_multiple = float(growth_multiple_list[0]) / 100
                    total_growth *= growth_multiple
                growth_per_prediction.append(total_growth * 100)
                # print(total_growth)
                # if total_growth != 1:
            growth_per_start_year.append(mean(growth_per_prediction))
        print(growth_per_start_year)
        growth_per_pred_type.append({'n': n, 'value': mean(growth_per_start_year)})
    print("using the n year prediction for 5 years without swapping")
    print(growth_per_pred_type)
    print("conclusing, 5 year prediction works best after 5 years of growth, shocker")