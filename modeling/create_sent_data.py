import pandas as pd
import sys
from random import randint

if __name__ == '__main__':
	fname = sys.argv[1]
	df = pd.read_json(fname)
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

