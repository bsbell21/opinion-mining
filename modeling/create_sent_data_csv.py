import pandas as pd
import sys
from random import randint
import ipdb
import csv
import json

'''
Ben's script to create sentiment data for the models, sentiment is randomly assigned - will eventually want to use 
real sentiment data
'''

if __name__ == '__main__':
	fname = sys.argv[1]
	output_fname = sys.argv[2]
	reader = csv.DictReader(open(fname))

	d_new = {'review_id': [], 'sentence': [], 'sentiment': []}

	sent = ['Positive', 'Objective', 'Negative']

	# ipdb.set_trace()

	for row in reader:
		sentences = row['text'].split('.')
		for sentence in sentences:
			d_new['review_id'].append(row['review_id'])
			d_new['sentence'].append(sentence)
			d_new['sentiment'].append(sent[randint(0,2)])







	# ipdb.set_trace()
	# for k in d:
	# 	sentences = d[k]['text'].split('.')
	# 	for sentence in sentences:
	# 		d_new['review_id'].append(k)
	# 		d_new['sentence'].append(sentence)
	# 		d_new['sentiment'].append(sent[randint(0,2)])

	with open(output_fname, "wb") as outfile:
	   writer = csv.writer(outfile)
	   writer.writerow(d_new.keys())
	   writer.writerows(zip(*d_new.values()))


	# with open(output_fname, 'wb') as f:  # Just use 'w' mode in 3.x
	#     w = csv.DictWriter(f, d_new.keys())
	#     w.writeheader()

	#     w.writerow(d_new)

	# df_sent = pd.DataFrame(d_new).T
	# df_sent.to_csv(output_fname)
	print 'success, created file: ' + output_fname



	# read the entire file into a python array
	# with open(fname, 'rb') as f:
	#     data = f.readlines()

	# # remove the trailing "\n" from each line
	# data = map(lambda x: x.rstrip(), data)

	# each element of 'data' is an individual JSON object.
	# i want to convert it into an *array* of JSON objects
	# which, in and of itself, is one large JSON object
	# basically... add square brackets to the beginning	
	# and end, and have all the individual business JSON objects
	# separated by a comma

	# ipdb.set_trace()
	# data_json_str = "[" + ','.join(data) + "]"
	# data_json_list = json.loads(data_json_str)



	# # df = pd.read_json(data_json_str)

	# # df = df.set_index('review_id')
	# # d = df.T.to_dict()


	# for entry in data_json_list:
	# 	sentences = entry['text'].split('.')
	# 	for sentence in sentences:
	# 		d_new['review_id'].append(entry['review_id'])
	# 		d_new['sentence'].append(sentence)
	# 		d_new['sentiment'].append(sent[randint(0,2)])
	# # ipdb.set_trace()




