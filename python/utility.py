#############################
# This module contains the functions for
# reading the datasets to the data structures.
#############################
from pandas import DataFrame, Series
import numpy as np
import os
import pycountry
import pandas as pd

#This functipon takes countries array and alpha code type
#and returns a dictionary array as key = name and value = alpha
def convert_countryname_to_alpha3(countries):
	for i, country in enumerate(countries): 
		try:
			countries[i] = pycountry.countries.get(name = country).alpha_3
		except:
			print("Error in converting to alpha 3 for country: " + country)
	return countries	

#This function replaces some shorthandes with formal names
def fix_commonname_to_formal(countries):
	countries[countries == 'Russia'] = 'Russian Federation'
	countries[countries == 'Iran'] = 'Iran, Islamic Republic of'
	countries[countries == 'Syria'] = 'Syrian Arab Republic'
	countries[countries == 'Czech Republic'] = 'Czechia'
	countries[countries == 'Bolivia'] = 'Bolivia, Plurinational State of'
	countries[countries == 'Bosnia-Herzegovina'] = 'Bosnia and Herzegovina'
	countries[countries == 'Venezuela'] = 'Venezuela, Bolivarian Republic of'
	countries[countries == 'Taiwan'] = 'Taiwan, Province of China'
	countries[countries == 'South Korea'] = 'Korea, Republic of'
	countries[countries == 'Democratic Republic of the Congo'] = 'Congo, The Democratic Republic of the'
	countries[countries == 'Republic of the Congo'] = 'Congo'
	countries[countries == 'Macedonia'] = 'Macedonia, Republic of'
	countries[countries == 'Ivory Coast'] = 'Côte d\'Ivoire'
	countries[countries == 'Moldova'] = 'Moldova, Republic of'
	countries[countries == 'Laos'] = 'Lao People\'s Democratic Republic'
	countries[countries == 'Tanzania'] = 'Tanzania, United Republic of'
	return countries
	
#This function reads terror database and creates a 
#pandas dataframe only consisting specified columns
def read_terror_db(path, columns):
	df = pd.read_excel(io = path, parse_cols = columns)
	return df

def write_df_to_csv(df,path):
	df.to_csv(path, columns = df.columns)	
