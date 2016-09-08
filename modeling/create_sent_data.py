import pandas as pd
import sys
from random import randint

if __name__ == '__main__':
	fname = sys.argv[1]

	# read the entire file into a python array
	with open(fname, 'rb') as f:
	    data = f.readlines()

	# remove the trailing "\n" from each line
	data = map(lambda x: x.rstrip(), data)

	# each element of 'data' is an individual JSON object.
	# i want to convert it into an *array* of JSON objects
	# which, in and of itself, is one large JSON object
	# basically... add square brackets to the beginning
	# and end, and have all the individual business JSON objects
	# separated by a comma
	data_json_str = "[" + ','.join(data) + "]"

	df = pd.read_json(data_json_str)
	
	df = df.set_index('review_id')
	d = df.to_dict()
	d_new = {'review_id': [], 'sentence': [], 'sentiment': []}
	sent = ['Positive', 'Neutral', 'Negative']
	for k, v in d:
		sentences = v['text'].split('.')
		for sentence in sentences:
			d_new['review_id'].append(k)
			d_new['sentence'].append(sentence)
			d_new['sentiment'].append(sent[randint(0,2)])

	df_sent = pd.DataFrame(d_new).T
	df_sent.to_json('Training' + fname)

