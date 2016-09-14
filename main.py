import json
import time
import pandas as pd
import json
import ipdb

# from pymongo import MongoClient
from classes.business import Business

def get_reviews_for_business(bus_id, df):
	"""
	INPUT: business id, pandas DataFrame
	OUTPUT: Series with only texts
	
	For a given business id, return the review_id and 
	text of all reviews for that business. 
	"""
	return df[df.business_id==bus_id]

def read_data():
	"""
	INPUT: None
	OUTPUT: pandas data frame from file
	"""
	return pd.read_csv('./data/yelp_data/processed.csv')

'''
ORIGINAL MAIN FUNCTION

def main(): 

	client = MongoClient()
	db = client.yelptest2
	summaries_coll = db.summaries	

	print "Loading data..."
	df = read_data()
	bus_ids = df.business_id.unique()[21:]

	for bus_id in bus_ids:

		print "Working on biz_id %s" % bus_id
		start = time.time()

		biz = Business(get_reviews_for_business(bus_id,df))
		summary = biz.aspect_based_summary()
		
		summaries_coll.insert(summary)

		print "Inserted summary for %s into Mongo" % biz.business_name

		elapsed = time.time() - start
		print "Time elapsed: %d" % elapsed

'''

def main(): 

	# client = MongoClient()
	# db = client.yelptest2
	# summaries_coll = db.summaries	

	list_of_summaries = [] #my addition

	print "Loading data..."
	df = read_data()
	bus_ids = df.business_id.unique()[21:] #why this slice? maybe remove

	for bus_id in bus_ids:

		print "Working on biz_id %s" % bus_id
		start = time.time()

		biz = Business(get_reviews_for_business(bus_id,df))
		summary = biz.aspect_based_summary()
		
		# summaries_coll.insert(summary)
		list_of_summaries.append(summary)


		print "Inserted summary for %s" % biz.business_name

		elapsed = time.time() - start
		print "Time elapsed: %d" % elapsed

	# my addition below

	# ipdb.set_trace()

	json_string = json.dumps(list_of_summaries)
	with open('data/summaries_data.txt', 'w') as outfile:
		json.dump(json_string, outfile)

	with open('data/summaries_data2.txt', 'w') as outfile:
		outfile.write(unicode(json.dumps(list_of_summaries, ensure_ascii=False)))



if __name__ == "__main__":
	main()



