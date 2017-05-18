import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import os
from utility import *
import utility as util

def generate_country_casualty_data():
	df = util.read_excel("../../Datasets/gtd_12to15_0616dist.xlsx", "I,CW")
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
	sums['casulties'] = sums['casulties'].astype(int)
	return sums

def generate_country_casualty_with_pctile():	
	df = generate_country_casualty_data()
	df['pctile'] = df.rank(pct = True)
	return df

df = generate_country_casualty_with_pctile()
df['ranking'] = df['casulties'] / df['pctile']	
util.write_df_to_csv(df, '../../Datasets/data.csv')

