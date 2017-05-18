# coding=utf-8
#############################
# This module contains the functions for
# reading the datasets to the data structures.
#############################
from pandas import DataFrame, Series
import pycountry
import pandas as pd
import csv
import json


# This functipon takes countries array and alpha code type
# and returns a dictionary array as key = name and value = alpha
def convert_countryname_to_alpha3(countries):
    for i, country in enumerate(countries):
        try:
            countries[i] = pycountry.countries.get(name = country).alpha_3
        except:
            #print("Error in converting to alpha 3 for country: " + country)
            pass
    return countries


# This function replaces some shorthandes with formal names
def fix_commonname_to_formal(countries):
    countries[countries == 'Russia'] = 'Russian Federation'
    countries[countries == 'Iran'] = 'Iran, Islamic Republic of'
    countries[countries == 'Syria'] = 'Syrian Arab Republic'
    countries[countries == 'Czech Republic'] = 'Czechia'
    countries[countries == 'Bolivia'] = 'Bolivia, Plurinational State of'
    countries[countries == 'Bosnia-Herzegovina'] = 'Bosnia and Herzegovina'
    countries[countries == 'Venezuela'] = 'VEN'
    countries[countries == 'Taiwan'] = 'Taiwan, Province of China'
    countries[countries == 'South Korea'] = 'Korea, Republic of'
    countries[countries == 'Democratic Republic of the Congo'] = 'COD'
    countries[countries == 'Republic of the Congo'] = 'Congo'
    countries[countries == 'Macedonia'] = 'Macedonia, Republic of'
    countries[countries == 'Ivory Coast'] = 'CIV'
    countries[countries == 'Moldova'] = 'Moldova, Republic of'
    countries[countries == 'Laos'] = 'Lao People\'s Democratic Republic'
    countries[countries == 'Tanzania'] = 'Tanzania, United Republic of'
    countries[countries == 'West Bank and Gaza Strip'] = 'Palestine, State of'
    return countries


# This function reads terror database and creates a
# pandas dataframe only consisting specified columns
def read_excel(path, columns):
    df = pd.read_excel(io = path, parse_cols = columns)
    return df


# This function read data from csv file and return pandas dataframe
def read_csv(path):
    df = pd.read_csv(path)
    return df


# This function write pandas dataframe to csv
def write_df_to_csv(df,path):
    df.to_csv(path, columns = df.columns)


# This function write list of data to csv
def write_data_to_csv(data, path):
    with open(path, 'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(["year", "country", "event_count"])
        for row in data:
            csv_out.writerow(row)
			
#this function filters the organizations and NGO'S
def filterCountries(codes):
    countryList = list() 
    for i, countryCode in enumerate(codes):
        try:
            countryList.append(pycountry.countries.get(alpha_3 = countryCode).alpha_3)
        except:
            print("not in list",countryCode)
    return countryList

def printCountries(codes):
    for i, countryCode in enumerate(codes):
        try:
            print(pycountry.countries.get(alpha_3 = countryCode).name)
        except:
            print("not in list",countryCode)

def change_country_names(countries):
    countries = fix_commonname_to_formal(countries)
    countries = convert_countryname_to_alpha3(countries)
    return countries


# return country dictionary which has neighbours of each country (ALPHA3)
def get_countries_neighbours():
    return json.loads(open('../Datasets/countries/neighbour.json').read())


