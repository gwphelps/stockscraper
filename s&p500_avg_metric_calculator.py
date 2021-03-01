import pandas
from statistics import mean
snp_df = pandas.read_csv('s&p500_growth_by_year.csv')
snp_df.set_index('year', inplace=True, drop=True)


pe_mean = []
fcf_mean = []
pb_mean = []
ps_mean = []
for year in range(2007, 2021):
    year_df = pandas.read_csv('yearlys&p/1_year/s&p500_pe_stock_nonratio_'+str(year)+'.csv')
    year_df.set_index('code', inplace=True, drop=True)

    #print(industry)
    #print(industry_codes)
    pe_mean.insert(0, year_df['initialPE'].mean())
    print(pe_mean)
    fcf_mean.insert(0, year_df['initialFCF'].mean())
    print(fcf_mean)
    pb_mean.insert(0, year_df['initialPB'].mean())
    print(pb_mean)
    ps_mean.insert(0, year_df['initialPS'].mean())
    print(ps_mean)
snp_df=snp_df.assign(initialPE=pe_mean)
snp_df=snp_df.assign(initialFCF=fcf_mean)
snp_df=snp_df.assign(initialPB=pb_mean)
snp_df=snp_df.assign(initialPS=ps_mean)
snp_df.to_csv('industry_averages/s&p500_growth_by_year.csv')



