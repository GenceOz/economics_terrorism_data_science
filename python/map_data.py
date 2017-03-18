import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import os
from utility import *
import utility as util

df = util.read_terror_db("../Datasets/gtd_12to15_0616dist.xlsx", "I,CW")
#Rename the columns
df.columns = ['countries','casulties']
#Calculate the sums for countires
grouped_by_country = df.groupby('countries')
sums = grouped_by_country.sum()
#Convert country names to alpha 3 codes
country_names = sums.index.values
country_names = util.fix_commonname_to_formal(country_names)
country_array = util.convert_countryname_to_alpha3(country_names)
sums.reindex(country_array)
#Clean the data
sums = sums.drop(['Kosovo', 'West Bank and Gaza Strip'])
sums = sums.fillna(0)
sums = sums.casulties.astype(int)
util.write_df_to_csv(sums.to_frame(), '../Datasets/data.csv')