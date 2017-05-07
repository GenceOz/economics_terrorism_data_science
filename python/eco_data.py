from utility import *
import utility as util
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm




# economy histogram
series = ['Military expenditure (% of GDP)']
df_eco = util.read_excel("Datasets/econData.xlsx", "B,C,AY,AZ,BA,BB,BC,BD,BE,BF,BG,BH")





df_eco.columns = ['country_code', 'series', '2006', '2007',
                  '2008', '2009', '2010', '2011',
                  '2012', '2013', '2014', '2015']

grouped_by_country = df_eco.groupby('country_code')
sums = grouped_by_country.sum()
country_codes = sums.index.values

#filters the organizations out 
country_codes = util.filterCountries(country_codes)


df_eco = df_eco[df_eco['series'].isin(series)]
df_eco = df_eco[df_eco['country_code'].isin(country_codes)]


#replaces every Nan value with .. and forms a new column Military Expenditure 
#and sums all of the column values per row
df_eco = df_eco.replace("..", np.NaN)
df_eco['Military expenditure'] = df_eco[['2006', '2007', '2008', '2009',
                                         '2010', '2011', '2012', '2013',
                                         '2014', '2015']].sum(axis=1)
del df_eco['series']
del df_eco['2006']
del df_eco['2007']
del df_eco['2008']
del df_eco['2009']
del df_eco['2010']
del df_eco['2011']
del df_eco['2012']
del df_eco['2013']
del df_eco['2014']
del df_eco['2015']
df_eco = df_eco.sort_values(by='Military expenditure', ascending=0)
df_eco = df_eco.head(20)
x = 'country_code'
y = 'Military expenditure'
kind = 'bar'
title = 'Top 20 Countries - Military expenditure (2006-2015)'
df_eco.plot(x=x, y=y, kind=kind, title=title)
plt.show()

#economy scatter
series = ['Foreign direct investment, net inflows (% of GDP)']

df_eco = util.read_excel("Datasets/econData.xlsx", "B,C,AY,AZ,BA,BB,BC,BD,BE,BF,BG,BH")





df_eco.columns = ['country_code', 'series', '2006', '2007',
                  '2008', '2009', '2010', '2011',
                  '2012', '2013', '2014', '2015']

grouped_by_country = df_eco.groupby('country_code')
sums = grouped_by_country.sum()
country_codes = sums.index.values

#filters the organizations out 
country_codes = util.filterCountries(country_codes)


df_eco = df_eco[df_eco['series'].isin(series)]
df_eco = df_eco[df_eco['country_code'].isin(country_codes)]

#replaces every Nan value with .. and forms a new column Military Expenditure 
#and sums all of the column values per row
df_eco = df_eco.replace("..", np.NaN)
df_eco['Foreign direct investment'] = df_eco[['2006', '2007', '2008', '2009',
                                         '2010', '2011', '2012', '2013',
                                         '2014', '2015']].sum(axis=1)
df_eco = df_eco.sort_values(by='Foreign direct investment', ascending=0)
df_eco = df_eco.head(20)

dates = ['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']
listbycountry = []
l = []

#this gets investments from 2006 to 2015 for each country code
for idx, val in enumerate(df_eco.index):
    for d in dates:
        listbycountry.append(df_eco.at[df_eco.index[idx],d])
    l.append(listbycountry)
    listbycountry = []
        
countryCode = []
countryCode = df_eco['country_code'].tolist()


x = np.arange(20)
ys = [i+x+(i*x)**2 for i in range(20)]

colors = cm.rainbow(np.linspace(0, 1, len(ys)))

fig = plt.figure()
ax1 = fig.add_subplot(111)


index = 0
colorOfpoints = 0

#this colors all of the investment according to years by country
for idx,val in enumerate(l):
    ax1.scatter(dates,val,s = 10,color = colors[index], marker="s", label=countryCode[index])
    plt.plot(dates, val, c=colors[index])
    index = index + 1

fig.set_size_inches(13.5, 10.5, forward=True)
ax1.set_xlabel('Years')
ax1.set_ylabel('Foreign direct investment, net inflows (% of GDP)')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5));
plt.show()        







