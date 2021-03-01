import pandas
from sklearn import linear_model
import matplotlib.pyplot as plt
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
for i in range(1, 6):

    df = pandas.read_csv('yearlys&p/'+str(i)+'_year_s&p500_pe_stock_ratio.csv')

    for industry in industries.keys():
        df2 = df[df['industry'] == industry]
        #print(df2)

        X = df2[['initialPE', 'initialFCF', 'initialPB', 'initialPS']]
        y = df2['stockratio']



        linear_mod = linear_model.LinearRegression()
        linear_mod.fit(X, y)
        #industryCoef = industry + " " + str(linear_mod.coef_[0]) + " " + str(linear_mod.intercept_)
        #print(industryCoef)
        industries[industry] = {
            'pe_c': linear_mod.coef_[0],
            'fcf_c': linear_mod.coef_[1],
            'pb_c': linear_mod.coef_[2],
            'ps_c': linear_mod.coef_[3],
            'intercept': linear_mod.intercept_
        }
    out_df = pandas.DataFrame(industries).T
    out_df['industry'] = out_df.index
    print(out_df)
    out_df.to_csv('yearlys&p/'+str(i)+'_year_s&p500_industry_equations.csv')


