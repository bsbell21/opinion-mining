import pandas as pd
import sys
from random import randint

if __name__ == '__main__':
	fname = sys.argv[1]
	df = pd.read_json(fname)
	sent = ['Positive', 'Neutral', 'Negative']
	df['sentiment'] = df['business_id'].apply(lambda x: sent[randint(0,2)])
	df.to_json('Training' + fname)

