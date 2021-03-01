import pandas
from statistics import mean
import numpy as np

df = pandas.read_csv('s&p500_daily_stats.csv')
df.set_index('code', inplace=True, drop=True)
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
    industries[industry] = {}

for industry in industries.keys():
    industries[industry]['pe-ratio'] = mean([df.at[stock, 'pe-ratio'] for stock in df.index.tolist() if df.at[stock, 'industry'] == industry])
    industries[industry]['price-fcf'] = mean([df.at[stock, 'price-fcf'] for stock in df.index.tolist() if df.at[stock, 'industry'] == industry])
    industries[industry]['price-book'] = mean([df.at[stock, 'price-book'] for stock in df.index.tolist() if df.at[stock, 'industry'] == industry])
    industries[industry]['price-sales'] = mean([df.at[stock, 'price-sales'] for stock in df.index.tolist() if df.at[stock, 'industry'] == industry])

    df.loc[(df['pe-ratio'] == 0), 'pe-ratio'] = industries[industry]['pe-ratio']
    df.loc[(df['price-fcf'] == 0), 'pe-ratio'] = industries[industry]['price-fcf']
    df.loc[(df['price-book'] == 0), 'pe-ratio'] = industries[industry]['price-book']
    df.loc[(df['price-sales'] == 0), 'pe-ratio'] = industries[industry]['price-sales']
mean_pe = df['pe-ratio'].mean(skipna=True)
print(mean_pe)
mean_fcf = df['price-fcf'].mean(skipna=True)
print(mean_fcf)
mean_pb = df['price-book'].mean(skipna=True)
print(mean_pb)
mean_ps = df['price-sales'].mean(skipna=True)
print(mean_ps)


df['pe-ratio'] = df['pe-ratio'] / mean_pe

df['price-fcf'] = df['price-fcf'] / mean_fcf
df['price-book'] = df['price-book'] / mean_pb
df['price-sales'] = df['price-sales'] / mean_ps
print(df)
df.to_csv('s&p500_daily_stats_adjusted.csv')
