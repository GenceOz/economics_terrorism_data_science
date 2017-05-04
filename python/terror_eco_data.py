import utility as util
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
This functions grouping all terror database by countries and years
and finds total terror events with corresponding grouping. At the end
csv file is created...
'''
def group_terrors_by_country_and_year():
    # group by year and countries, aggregate size of them
    df = util.read_excel("../Datasets/globalterrorismdb_0616dist.xlsx", "B,I")
    df.columns = ['year', 'countries']
    group_by_year_country = df.groupby(['year', 'countries'])
    sizes = group_by_year_country.size()
    data = sizes.index.values
    counts = sizes.values

    # HACK: add aggregate count of grouping by year and countries to data.
    for i, count in enumerate(counts):
        data[i] += (count,)

    util.write_data_to_csv(data, '../Datasets/terror_event_years.csv')


'''
This function takes 2 inputs
Input 1: begin year to take data
Input 2: end year to take data
This function read csv file created by function group_terrors_by_country_and_year()
and grouping that data by countries and find total terror event for corresponding country
'''
def group_terror_by_countries(begin_year, end_year):
    df = util.read_csv('../Datasets/terror_event_years.csv')
    df.columns = ['year', 'country_code', 'terror_event']
    # filtering data based on years
    df = df[df['year'] >= begin_year]
    df = df[df['year'] <= end_year]
    grouped_by_country = df.groupby('country_code')
    sums = grouped_by_country.sum()
    country_names = sums.index.values
    country_names = util.fix_commonname_to_formal(country_names)
    country_array = util.convert_countryname_to_alpha3(country_names)
    sums.reindex(country_array)

    # TODO: distinguish between dates to drop countries.
    # this is for 1970 - 2015 data
    # sums = sums.drop(
    #     ['Kosovo', 'Macau', 'New Hebrides', 'North Korea', 'North Yemen', 'People\'s Republic of the Congo',
    #      'Rhodesia', 'Serbia-Montenegro', 'Slovak Republic', 'South Vietnam', 'South Yemen', 'Soviet Union',
    #      'St. Kitts and Nevis', 'St. Lucia', 'Vatican City', 'Vietnam', 'West Bank and Gaza Strip',
    #      'West Germany (FRG)', 'Yugoslavia', 'Zaire'])

    # this is for 2012 - 2015 data
    sums = sums.drop(['Kosovo', 'West Bank and Gaza Strip'])

    sums = sums.terror_event.astype(int)
    # sorting the sums
    sums = sums.sort_values(ascending=0)
    util.write_df_to_csv(sums.to_frame(), '../Datasets/terror_event_total_{}_{}.csv'.format(begin_year, end_year))


'''
This function is merging two data sets and plots a diagram to show
two data sets into one diagram and their correlations.
'''
# TODO: This function should be generic based on years and specific column of economic data
def plot_terror_economy():
    # terror phase
    begin_year = 2012
    end_year = 2015

    df_terror = pd.read_csv('../Datasets/terror_event_total_{}_{}.csv'.format(begin_year, end_year))
    # taking specific number of country
    # df_terror = df_terror.head(100)

    df_terror = df_terror.sort_values(by='country_code')
    df_terror_countries = df_terror.country_code.values

    # economy phase
    series = ['GDP (current US$)']

    # TODO: change columns based on begin and end years
    df_eco = util.read_excel("../Datasets/eco.xlsx", "B,C,BE,BF,BG,BH")
    df_eco.columns = ['country_code', 'series', '2012', '2013', '2014', '2015']

    # filter based on series and countries terror occurs
    df_eco = df_eco[df_eco['series'].isin(series)]
    df_eco = df_eco[df_eco['country_code'].isin(df_terror_countries)]
    df_eco = df_eco.replace(0, np.NaN)

    # mean of GDP between corresponding years
    df_eco['GDP'] = df_eco[['2012', '2013', '2014', '2015']].mean(axis=1)

    # delete unnecessary columns
    del df_eco['series']
    del df_eco['2012']
    del df_eco['2013']
    del df_eco['2014']
    del df_eco['2015']

    df_eco = df_eco.sort_values(by='country_code')
    path = '../Datasets/terror_economy_{}_{}_{}.csv'.format(series[0], begin_year, end_year)

    # merge datasets phase
    df = pd.concat([df_terror.set_index('country_code'), df_eco.set_index('country_code')], axis=1, join='inner')
    df = df.reset_index()
    df.to_csv(path, mode='w', index=False)

    # plotting the diagram
    x = 'terror_event'
    y = 'GDP'
    kind = 'scatter'
    title = 'GDP - Terror in Countries (2012-2015)'
    df.plot(x=x, y=y, kind=kind, title=title)
    plt.show()

'''
This function plots 20 most countries with terrors between
two input years.
'''
def plot_most_terror_areas(begin_year, end_year):
    df = pd.read_csv('../Datasets/terror_event_average_{}_{}.csv'.format(begin_year, end_year))
    df = df.head(20)
    x = 'country_code'
    y = 'terror_event'
    kind = 'bar'
    title = 'Top 20 Countries - Terror Event (1970-2015)'
    df.plot(x=x, y=y, kind=kind, title=title)
    plt.show()


'''
This function is plotting economy data corresponding series and years
'''
# TODO: this function should be more specefic to determine years of data
def plot_economy_data():
    series = ['Military expenditure (% of GDP)']

    # TODO: change columns based on begin and end years
    df_eco = util.read_excel("../Datasets/eco.xlsx", "B,C,AY,AZ,BA,BB,BC,BD,BE,BF,BG,BH")
    df_eco.columns = ['country_code', 'series', '2006', '2007',
                      '2008', '2009', '2010', '2011',
                      '2012', '2013', '2014', '2015']
    df_eco = df_eco[df_eco['series'].isin(series)]
    df_eco = df_eco.replace(0, np.NaN)

    # sum of military expenditure (% GDP)
    df_eco['Military expenditure'] = df_eco[['2006', '2007', '2008', '2009',
                                             '2010', '2011', '2012', '2013',
                                             '2014', '2015']].sum(axis=1)

    # remove unnecessary columns
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

# tests
group_terrors_by_country_and_year()
group_terror_by_countries(2012, 2015)
plot_terror_economy()
plot_economy_data()
