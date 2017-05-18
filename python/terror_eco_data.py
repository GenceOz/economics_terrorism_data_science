import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import itertools
import utility

'''
This functions grouping all terror database by countries and years
and finds total terror events with corresponding grouping. At the end
csv file is created...
'''


def group_terrors_by_country_and_year():
    csv_read_path = "../Datasets/gtd_92to11_0616dist.xlsx"
    csv_write_path = '../Datasets/terror_event_years_1992_2011.csv'

    # group by year and countries, aggregate size of them
    df = utility.read_excel(csv_read_path, "B,I,CW")
    df.columns = ['year', 'country_code', "event_count"]
    df = df.groupby(['year', 'country_code']).count()
    utility.write_df_to_csv(df, csv_write_path)

    # read previous csv change country names
    df = utility.read_csv(csv_write_path)

    # drops some countries
    df = df[df.country_code != "West Bank and Gaza Strip"]
    df = df[df.country_code != "Kosovo"]

    df.country_code.values[:] = utility.change_country_names(df.country_code.values)[:]
    utility.write_df_to_csv(df, csv_write_path)


'''
This function takes 2 inputs
Input 1: begin year to take data
Input 2: end year to take data
This function read csv file created by function group_terrors_by_country_and_year()
and grouping that data by countries and find total terror event for corresponding country
'''


def group_terror_by_countries(begin_year, end_year):
    df = utility.read_csv('../Datasets/terror_event_years.csv')
    df.columns = ['year', 'country_code', 'terror_event']
    # filtering data based on years
    df = df[df['year'] >= begin_year]
    df = df[df['year'] <= end_year]
    grouped_by_country = df.groupby('country_code')
    sums = grouped_by_country.sum()
    country_names = sums.index.values
    country_names = utility.fix_commonname_to_formal(country_names)
    country_array = utility.convert_countryname_to_alpha3(country_names)
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
    utility.write_df_to_csv(sums.to_frame(), '../Datasets/terror_event_total_{}_{}.csv'.format(begin_year, end_year))


'''
prepare the economy data between 2012 and 2015,
countries should be included in terror data
'''


def prepare_economy_data():
    df_terror = utility.read_csv('../Datasets/terror_event_years_2012_2015.csv')
    df_eco = utility.read_excel("../Datasets/eco.xlsx", "B,C,BE,BF,BG,BH")
    df_eco.columns = ['country_code', 'series', '2012', '2013', '2014', '2015']

    df_eco = df_eco[df_eco['country_code'].isin(df_terror.country_code.values)]

    df_eco = pd.melt(df_eco, id_vars=["country_code", "series"], value_vars=["2012", "2013", "2014", "2015"])
    df_eco.columns = ["country_code", "series", "year", "value"]
    df_eco = df_eco[df_eco.value != 0]
    df_eco = df_eco.set_index(["year", "country_code", "series"])
    df_eco = df_eco['value'].unstack('series')

    utility.write_df_to_csv(df_eco, "../Datasets/2012-2015-eco.csv")


'''
This function is merging two data sets (terror and economy) with intended columns of data
then create new csv from them.
'''


def merge_terror_economy():
    df_terror = utility.read_csv("../Datasets/2012-2015-terror.csv")
    df_eco = utility.read_csv("../Datasets/2012-2015-eco.csv")

    df_terror = df_terror.set_index(['year', 'country_code'])
    df_eco = df_eco.set_index(['year', 'country_code'])

    df = df_terror.join(df_eco)

    df.columns = ['terror_count', 'armed',
                  'arms_import', 'exports',
                  'foreign_in_invesment', 'gdp_growth',
                  'gdp_per_capita', 'gross_expenditure',
                  'public_health_expenditure',
                  'total_health_expenditure', 'imports', 'life_expectancy']

    df = df.dropna()

    utility.write_df_to_csv(df, '../Datasets/2012-2015-terror-eco.csv')

    # plotting the diagram
    # x = 'event_count'
    # y = 'gdp_growth'
    # kind = 'scatter'
    # title = 'GDP Growth - Event Number (2012-2015)'
    # df.plot(x=x, y=y, kind=kind, title=title)
    # plt.show()


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


def plot_economy_data():
    series = ['Military expenditure (% of GDP)']

    df_eco = utility.read_excel("../Datasets/eco.xlsx", "B,C,AY,AZ,BA,BB,BC,BD,BE,BF,BG,BH")
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


'''
This function calculates best model with given economy data
parameter is defined as how many economical data will be in regression
Best R_valued regression model is returned
'''


def print_max_R_valued_relations(number_of_eco_data):
    df = pd.read_csv('../Datasets/2012-2015-terror-eco.csv')
    df = df.set_index(['year', 'country_code'])
    features = list(df.columns[1:])
    y = df.terror_count

    lm = LinearRegression()
    temp = list(itertools.combinations(features, number_of_eco_data))
    max__r = 0
    max__r_list = []
    for t in temp:
        X = df[list(t)]
        lm.fit(X, y)
        if lm.score(X, y) > max__r:
            max__r = lm.score(X, y)
            max__r_list = list(t)
    print(max__r, max__r_list)


'''
This function prepare neighbour data csv,
chosen neighbour is country that has most terrorist attack at that year
If data of neighbour is not available, data will be own data of country
'''


def prepare_neighbour_data():
    df = pd.read_csv('../Datasets/2012-2015-terror-eco-hypo.csv')
    df = df.set_index(['year', 'country_code'])
    df['arms_import_neighbour'] = np.NaN
    df['gdp_growth_neighbour'] = np.NaN
    df['life_expectancy_neighbour'] = np.NaN
    for index, row in df.iterrows():
        year = index[0]
        country_code = index[1]

        neighbours = utility.get_countries_neighbours().get(country_code, None)
        if neighbours is not None:
            max_terror = 0
            max_neighbour = ''
            for neighbour in neighbours:
                try:
                    terror = df.xs([year, neighbour]).terror_count
                    if terror > max_terror:
                        max_terror = terror
                        max_neighbour = neighbour
                except:
                    # print('error', year, neighbour)
                    continue
            if max_neighbour != '':
                df.set_value(index, 'arms_import_neighbour', df.xs([year, max_neighbour]).arms_import)
                df.set_value(index, 'gdp_growth_neighbour', df.xs([year, max_neighbour]).gdp_growth)
                df.set_value(index, 'life_expectancy_neighbour', df.xs([year, max_neighbour]).life_expectancy)
            else:
                df.set_value(index, 'arms_import_neighbour', df.xs([year, country_code]).arms_import)
                df.set_value(index, 'gdp_growth_neighbour', df.xs([year, country_code]).gdp_growth)
                df.set_value(index, 'life_expectancy_neighbour', df.xs([year, country_code]).life_expectancy)
        else:
            df.set_value(index, 'arms_import_neighbour', df.xs([year, country_code]).arms_import)
            df.set_value(index, 'gdp_growth_neighbour', df.xs([year, country_code]).gdp_growth)
            df.set_value(index, 'life_expectancy_neighbour', df.xs([year, country_code]).life_expectancy)
    df.to_csv('../Datasets/2012-2015-terror-eco-hypo-neighbour.csv')


'''
training with 2012-2015 data and tested with 2011 data and return it.
'''


def calculate_mae_mse():
    df_hypo = pd.read_csv('../Datasets/2012-2015-terror-eco-hypo.csv')
    df_test = pd.read_csv('../Datasets/2011-terror-eco-test.csv')

    lm = smf.ols(formula='terror_count ~ arms_import + gdp_growth + life_expectancy', data=df_hypo).fit()
    params = list(df_test.columns[3:])
    prediction = lm.predict(df_test[params])
    real = list(df_test.terror_count)
    mae = mean_absolute_error(real, prediction)
    mse = mean_squared_error(real, prediction)
    return mae, mse


'''
linear regression with specific economy data with terror event count
'''


def linear_regression(param):
    df_hypo = pd.read_csv('../Datasets/2012-2015-terror-eco-hypo.csv')
    lm = smf.ols(formula='terror_count ~ ' + param, data=df_hypo).fit()
    print(lm.summary())
    X_new = pd.DataFrame({param: [df_hypo[param].min(), df_hypo[param].max()]})
    preds = lm.predict(X_new)
    df_hypo.plot(kind='scatter', x=param, y='terror_count')
    plt.plot(X_new, preds, c='red', linewidth=3)
    plt.show()


'''
Multi regression of terror_count ~ arms_import + gdp_growth + life_expectancy
'''


def multi_regression():
    df_hypo = pd.read_csv('../Datasets/2012-2015-terror-eco-hypo.csv')
    lm = smf.ols(formula='terror_count ~ arms_import + gdp_growth + life_expectancy', data=df_hypo).fit()
    print(lm.summary())
    print(calculate_mae_mse())


'''
Multi regression of terror_count ~ arms_import + gdp_growth + life_expectancy
and economic data of country who has most terrorist attack
'''


def multi_regression_with_neighbour_data():
    df_hypo = pd.read_csv('../Datasets/2012-2015-terror-eco-hypo-neighbour.csv')
    lm = smf.ols(formula='terror_count ~ arms_import + gdp_growth + life_expectancy '
                         '+ arms_import_neighbour + '
                         'gdp_growth_neighbour + life_expectancy_neighbour', data=df_hypo).fit()
    print(lm.summary())

# data cleaning and preparation
# group_terrors_by_country_and_year()
# group_terror_by_countries(2012, 2015)
# prepare_economy_data()
# merge_terror_economy()

# modelling
# linear_regression('arms_import')
# linear_regression('gdp_growth')
# linear_regression('life_expectancy')
# multi_regression()
# prepare_neighbour_data()
# multi_regression_with_neighbour_data()

# research about data
# plot_most_terror_areas(2012, 2015)
# plot_economy_data()
# print_max_R_valued_relations(3)
