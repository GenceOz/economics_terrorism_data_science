#This script clusters countries considering their total casulties
#over the years, it utilizes k-means algorithm to perform the clustring
from kmeans import KMeans
import utility as util
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import vector as vec 

def squared_clustering_errors(inputs, k):
	"""finds the total squared error from k-means clustering the inputs"""
	clusterer = KMeans(k)
	clusterer.train(inputs)
	means = clusterer.means
	assignments = map(clusterer.classify, inputs)

	return sum(vec.squared_distance(input, means[cluster])
       for input, cluster in zip(inputs, assignments))

def find_optimal_k_value(inputs, max_k_value):
	ks = range(1, max_k_value + 1)
	errors = [squared_clustering_errors(inputs, k) for k in ks]

	plt.plot(ks, errors)
	plt.xticks(ks)
	plt.xlabel("k")
	plt.ylabel("total squared error")
	plt.title("Total Error vs. # of Clusters")
	plt.show()


def cluster_countries(year_to_cluster, df):
	#Filter the year 
	df = df[df['iyear'] == 2012]
	#Rename the columns
	df.columns = ['iyear','countries','casulties']

	#Convert the country names to alpha3 format 
	country_names = np.array(df['countries'].tolist())
	country_names = util.fix_commonname_to_formal(country_names)
	country_names = util.convert_countryname_to_alpha3(country_names)
	df['countries'] = country_names

	#Calculate the sums for countires for each year
	grouped_by_country = df.groupby(['countries','iyear'])
	total_casulty_target_year = grouped_by_country.sum()
	total_casulty_target_year['casulties'] = total_casulty_target_year['casulties'].fillna(0.0).astype(int)
	data_points = total_casulty_target_year.values

	#find_optimal_k_value(data_points, 8)
	#Run the kmeans algorithm with the casulty values
	clusterer = KMeans(8)
	cluster_points = clusterer.train(data_points)

	del total_casulty_target_year['casulties']
	total_casulty_target_year['cluster'] = cluster_points

	total_casulty_target_year.to_csv('Data/clusters-{}.csv'.format(year_to_cluster), columns = total_casulty_target_year.columns)

def cluster_countries_between_year(start, end):
	if start < 2000 or start > 2015 or end < 2000 or end > 2015:
		print("The years are not in the datasets")
		return 1
	if start < 2012 and start > 2000 and end > 2012:
		#Read from the 91-11 database
		df = util.read_excel("../../Datasets/gtd_92to11_0616dist.xlsx", "B,I,CW")
		for i in range(start, 2012):
			cluster_countries(i, df)
		#Read from the 11-15 database
		df = util.read_excel("../../Datasets/gtd_12to15_0616dist.xlsx", "B,I,CW")
		for i in range(2012, end):
			cluster_countries(i, df)
	elif start < 2012 and start > 2000 and end < 2012:
		#Read from the 91-11 database
		df = util.read_excel("../../Datasets/gtd_92to11_0616dist.xlsx", "B,I,CW")
		for i in range(start, end + 1):
			cluster_countries(i, df)
	else: 
		#Read from the first database
		df = util.read_excel("../../Datasets/gtd_12to15_0616dist.xlsx", "B,I,CW")
		for i in range(start, end + 1):
			print("Clustering countries for year {}".format(i))
			cluster_countries(i, df)	

cluster_countries_between_year(2012, 2012)			
		
