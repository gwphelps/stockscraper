import pandas

df = pandas.read_csv('5_year_prediction_actual.csv')

def remove_highest_stats(data):
    #remove lowest PB - (presumed to be negative)






    return data

def reduce_to_10(data):
    #remove stock with highest value for each stat - 4
    data = remove_highest_stats(data)
    return sorted(data, key=lambda i: i['prediction'], reverse=True)[0:10]
    #remove stocks with 2 or more zeroes in the stat categories
    #reduce remaining to 10 by rank