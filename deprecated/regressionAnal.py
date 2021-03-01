import csv
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt

#plan: each company will be one pair of data points, with the
#dependent variable being the end stock price / beginning stock price
# in a 5 year period, and the independent variable being the initial pe ratio
#I think I might try and use peg ratio instead since that supposedly accounts for growth
MULTIPLIER = 1.5
industries = {}
def computeGoodPE(coeff, intercept, industry):
    pe = (MULTIPLIER-intercept) / coeff

    with open('good_pe_per_industry.csv', 'a', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow([industry, pe])


def get_data(filename):
    with open(filename, newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader)
        for row in reader:
            industry = row[1]
            if industry not in industries.keys():
                industries[industry] = []
                industries[industry].append([])
                industries[industry].append([])
                industries[industry].append([])
            industries[industry][0].append(float(row[2]))
            industries[industry][1].append(float(row[3]))


    return

def show_plot(dates,prices, industry):
    linear_mod = linear_model.LinearRegression()
    #dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
    #prices = np.reshape(prices,(len(prices),1))
    linear_mod.fit(dates,prices) #fitting the data points in the model
    print(linear_mod.coef_)
    print(linear_mod.intercept_)
    computeGoodPE(linear_mod.coef_, linear_mod.intercept_, industry)
    plt.scatter(dates,prices,color='yellow') #plotting the initial datapoints
    plt.plot(dates,linear_mod.predict(dates),color='blue',linewidth=3) #plotting the line made by linear regression
    plt.show()
    return

def predict_price(dates,prices,x):
    linear_mod = linear_model.LinearRegression() #defining the linear regression model
    dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
    prices = np.reshape(prices,(len(prices),1))
    linear_mod.fit(dates,prices) #fitting the data points in the model
    predicted_price =linear_mod.predict(x)
    return predicted_price[0][0],linear_mod.coef_[0][0] ,linear_mod.intercept_[0]

get_data("s&p500_pe_stock_ratio_no_outliers.csv")
print(industries.keys())
for industry in industries.keys():
    print(industry)
    show_plot(industries[industry][0], industries[industry][1], industry)

